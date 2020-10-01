import time
import random
import requests
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By

import json

url = 'https://www.fiverr.com/'

def init():
  option = Options()
  option.headless = False

  driver = webdriver.Firefox(options=option)
  driver.capabilities = webdriver.DesiredCapabilities.FIREFOX
  driver.capabilities['marionette'] = True

  return driver


driver = init()

driver.get(url)
time.sleep(random.random())

search_box = driver.find_element(By.XPATH, "//div[@class='header']//input[@type='search']")
time.sleep(random.random())
search_box.click()

search_box.send_keys('p')
time.sleep(random.random())

search_box.send_keys('h')
time.sleep(random.random())

search_box.send_keys('p')
time.sleep(random.random())


driver.quit()

