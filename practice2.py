import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import pyodbc
import datetime

# 存取今日日期
today = datetime.date.today()

# 連接資料庫
server = 'userTwhs\SQLEXPRESS'
database = 'stockinformation'
connection_string = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={server};DATABASE={database};Trusted_Connection=yes;'

conn = pyodbc.connect(connection_string)

# 建立游標
cursor = conn.cursor()

# 創建一個資料表，用來存取今日抓取下來的資料
create_table_query = '''
create table f'{today}ETF' (
    date ,
    ranking ,
    name ,
    number ,
    price ,
    highest ,
    lowest ,
)
'''

# 抓取網頁內容
volume = 'https://tw.stock.yahoo.com/tw-etf/volume'
res = requests.get(volume)
soup = bs(res.text, 'lxml')

# 創建資料存取處
data = []

# 尋找網頁中的具有所需資料的列表並提取列資料
table = soup.find(class_='M(0) P(0) List(n)')
lines = table.find_all(class_='List(n)')

# 建立序號
n = 1

# 抓取每一列中的欄資料，再抓取日期並添加序號後加在每一列資料的最前面
for line in lines:
    cols = line.find_all('div')
    cols = [col.text.strip() for col in cols]
    date = soup.find(class_='C(#6e7780) Fz(14px) As(fe)')
    date = str(date.text.strip())
    date = date.replace('資料時間：', '')
    date = date + f'_{str(n)}'
    n += 1
    cols.insert(0, date)
    data.append(cols)

# 將資料轉成表格形式，僅顯示需要的欄位
DF = pd.DataFrame(data)
DF = DF.dropna()
pd.set_option('display.max_columns', None)
DF.columns = ['日期', '', '', '名次', '', '', '', '股名', '股號', '股價', '漲跌', '漲跌幅(%)', '最高', '最低', '價差', '成交量']
DF2 = DF[['日期', '名次', '股名', '股號', '股價', '漲跌', '漲跌幅(%)', '最高', '最低', '價差', '成交量']]

DF2.to_excel('成交量.xlsx', sheet_name='工作表1', index=False, startrow=1)
