import requests
from bs4 import BeautifulSoup as bs
import pandas
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

names = driver.find_elements(By.CLASS_NAME, "prdName")
names = [names.text() for name in names]
prices = driver.find_elements(By.TAG_NAME, "b")
prices = [prices.text() for price in prices]
'''for commodity in name:
    print(commodity.text)
'''
time.sleep(5)
