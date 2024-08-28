import requests
from bs4 import BeautifulSoup as bs
import pyodbc
import datetime

# 抓取網頁內容
volumeweb = 'https://tw.stock.yahoo.com/tw-etf/volume'
res = requests.get(volumeweb)
soup = bs(res.text, 'lxml')

# 抓取表格類型
tabletype = soup.find(class_='Fz(24px) Fz(20px)--mobile Fw(b)')
tabletype = tabletype.get_text()

# 存取今日日期
today = str(datetime.date.today())

# 設定資料表名稱
tablename = tabletype + today

# 連接資料庫
server = r'userTwhs\SQLEXPRESS'
database = 'stockinformation'
username = 'testaccount'
password = 'Ab1234!?'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}'

conn = pyodbc.connect(connection_string)

# 建立游標
cursor = conn.cursor()

# 若資料表存在 先刪除
cursor.execute(f"IF OBJECT_ID('[{tablename}]', 'U') IS NOT NULL DROP TABLE [{tablename}]")

# 創建一個資料表，用來存取今日抓取下來的資料
create_table_query = f'''
create table [{tablename}] (
    date DATE NOT NULL,
    ranking INT PRIMARY KEY IDENTITY(1, 1),
    name NVARCHAR(50) NOT NULL,
    number NVARCHAR(50) NOT NULL,
    price DECIMAL(7, 2) NOT NULL,
    high DECIMAL(7, 2) NOT NULL,
    low DECIMAL(7, 2) NOT NULL,
    Spread DECIMAL(7, 2) NOT NULL,
    volume NVARCHAR(50) NOT NULL
)
'''
# 執行創建資料表
cursor.execute(create_table_query)

# 提交變更
conn.commit()

# 創建資料存取處
data = []

# 尋找網頁中的具有所需資料的列表並提取列資料
table = soup.find(class_='M(0) P(0) List(n)')
lines = table.find_all(class_='List(n)')

# 抓取每一列中的欄資料，再抓取日期並添加序號後加在每一列資料的最前面
for line in lines:
    cols = line.find_all('div')
    cols = [col.text.strip() for col in cols]
    data.append(cols)

# 過濾需要的資料
filter_data = [item[6:9] + item[11:15] for item in data]

# 將過濾過的資料依序插入資料表中
for record in filter_data:
    insert_query = f'''
    INSERT INTO [{tablename}](date, name, number, price, high, low, Spread, volume)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    '''
    cursor.execute(insert_query, (today, record[0], record[1], record[2], record[3], record[4], record[5], record[6]))
    conn.commit()

# 關閉連接
cursor.close()
conn.close()
