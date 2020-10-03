import requests
import os
import time
import datetime
import calendar
import json
import random
import re

from datetime import datetime

from selenium import webdriver
import undetected_chromedriver as uc

uc.TARGET_VERSION = 85
uc.install()

from selenium.webdriver import Chrome
from selenium.webdriver import Chrome, ChromeOptions

def createDataFolder():
  folderName = 'data'
  if not os.path.exists(folderName):
    os.makedirs(folderName)

def saveSearchToFile(name, searchResult):
  filename = f'data/{name}.json'
  with open(filename, 'w', encoding='utf-8') as fp:
    js = json.dumps(searchResult, indent=2)
    fp.write(js)

def fiverrApiSearchOmnibox(term, pro):
  r = requests.get(f'https://www.fiverr.com/search/layout/omnibox?callback=autocompleteCallback&from_medusa_header=true&pro_only={pro}&query={term}')
  return r.json()

def fiverrApiSearchRecommendation(term):
  # Simulate Chrome navigation
  randomNumber = random.random()

  headers = {
    'User-Agent': f'Mozilla/4.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.0.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 {randomNumber}',
    'upgrade-insecure-requests': '0',
    'sec-fetch-user': '?1',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document'
  }

  r = requests.get(f'https://www.fiverr.com/recommendations/related_search_terms?search_term={term}', headers=headers)
  return r.json()

def getSearchMetadata():
  utcNow = datetime.utcnow()
  isodate = datetime.fromtimestamp(utcNow.timestamp()).isoformat()
  timestamp = utcNow.timestamp()
  isodateString = str(isodate)

  result = {
    'timestamp': timestamp,
    'isodate': isodateString
  }

  return result

def searchBasicRecommendations(term):
  json = fiverrApiSearchOmnibox(term, True)
  metadata = getSearchMetadata()

  data = {
    'data': json
  }

  result = { **metadata, **data }

  return result

def searchAdvancedRecomendations(term):
  json = fiverrApiSearchRecommendation(term)
  metadata = getSearchMetadata()

  data = {
    'data': json
  }

  result = { **metadata, **data }
  
  return result


createDataFolder()

term = 'php'

basicSearch = searchBasicRecommendations(term)
advancedSearch = searchAdvancedRecomendations(term)

saveSearchToFile('basic_search', basicSearch)
saveSearchToFile('advanced_search', advancedSearch)


opts = ChromeOptions()
opts.add_argument('--no-sandbox')
opts.add_argument('--disable-dev-shm-usage')
opts.headless = False

driver = Chrome(options=opts)

driver.get(f'https://www.fiverr.com/search/gigs?query={term}&source=top-bar&search_in=everywhere&search-autocomplete-original-term={term}')
numberOfResultsElement = driver.find_element_by_xpath("//div[@class='number-of-results']")

html_content = numberOfResultsElement.get_attribute('innerHTML')
parsedTotalServiceList = re.findall(r'\d+', html_content)
totalServicesString = parsedTotalServiceList[0] + parsedTotalServiceList[1]

print(html_content)
print(totalServicesString)

driver.quit()