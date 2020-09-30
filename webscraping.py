import time
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

import json

url = 'https://stats.nba.com/players/traditional/?sort=PTS&dir=-1'

option = Options()
option.headless = True
binary = FirefoxBinary('/usr/bin/firefox')
driver = webdriver.Firefox()

driver.get(url)
# time.sleep(5)

driver.find_element_by_xpath("//div//div[@class='banner-actions-container']//button").click()
time.sleep(1)

# driver.find_element_by_xpath("//div[@class='nba-stat-table']//table//thead//tr//th[@data-field='PTS']").click()

element = driver.find_element_by_xpath("//div[@class='nba-stat-table']//table")
html_content = element.get_attribute('outerHTML')

soup = BeautifulSoup(html_content, 'html.parser')
table = soup.find(name='table')

df_full = pd.read_html(str(table))[0].head(10)
df = df_full[['Unnamed: 0', 'PLAYER', 'TEAM', 'PTS']]
df.columns = ['pos', 'player', 'team', 'total']

print(df)


driver.quit()