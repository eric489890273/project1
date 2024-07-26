import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

volume = 'https://tw.stock.yahoo.com/tw-etf/volume'
res = requests.get(volume)
soup = bs(res.text, 'lxml')

data = []

table = soup.find(class_='M(0) P(0) List(n)')
lines = table.find_all(class_='List(n)')

for line in lines:
    cols = line.find_all('div')
    cols = [col.text.strip() for col in cols]
    data.append(cols)

DF = pd.DataFrame(data)
DF = DF.dropna()
pd.set_option('display.max_columns', None)
DF.columns = ['', '', '名次', '', '', '', '股名', '股號', '股價', '漲跌', '漲跌幅(%)', '最高', '最低', '價差', '成交量']
DF2 = DF[['名次', '股名', '股號', '股價', '漲跌', '漲跌幅(%)', '最高', '最低', '價差', '成交量']]
print(DF2)

DF2.to_excel('成交量.xlsx', sheet_name='工作表1', index=False, startrow=1)
