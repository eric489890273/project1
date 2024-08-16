'''print("hello")

# 將資料轉成表格形式，僅顯示需要的欄位
DF = pd.DataFrame(data)
DF = DF.dropna()
pd.set_option('display.max_columns', None)
DF.columns = ['', '', '名次', '', '', '', '股名', '股號', '股價', '漲跌', '漲跌幅(%)', '最高','最低', '價差', '成交量']
DF2 = DF[['股名', '股號', '股價', '漲跌', '漲跌幅(%)', '最高', '最低', '價差', '成交量']]


# 儲存為 Excel 文件
DF2.to_excel('成交量.xlsx', sheet_name='工作表1', index=False, startrow=1)
'''
