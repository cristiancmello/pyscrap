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

driver.quit()