import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time

momo = "https://www.momoshop.com.tw/main/Main.jsp"

driver = webdriver.Chrome()
driver.get(momo)
KW = (By.ID, 'keyword')
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(KW),
)

search = driver.find_element(By.ID, 'keyword')
search.send_keys("顯卡")
search.send_keys(Keys.RETURN)
CT = (By.CLASS_NAME, "columnType")
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located(CT),
)

columntype = driver.find_element(By.CLASS_NAME, "columnType")
columntype.click()

rownames = driver.find_elements(By.CLASS_NAME, "prdName")
names = []
for rowname in rownames:
    names.append(rowname.text.strip())

rowprices = driver.find_elements(By.TAG_NAME, "b")
prices = []
for rowprice in rowprices:
    prices.append(rowprice.text.strip())

product = list(zip(names, prices))
table = pd.DataFrame(product)
table = table.dropna()
pd.set_option('display.max_columns', None)
table.columns = ['品名', '價格']
print(table)

table.to_excel('顯卡價格.xlsx', sheet_name='工作表1', index=False, startrow=1)

time.sleep(5)
