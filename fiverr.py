import requests
import os
import time
import datetime
import calendar
import json
import random
import re

import undetected_chromedriver as uc

from datetime import datetime
from random import choice
from selenium import webdriver
from fake_useragent import UserAgent

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

desktop_agents = ['Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/602.2.14 (KHTML, like Gecko) Version/10.0.1 Safari/602.2.14',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.98 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36',
                 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:50.0) Gecko/20100101 Firefox/50.0']
 
def random_headers():
    headers = {
      'User-Agent': UserAgent().random,
      'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
      'upgrade-insecure-requests': '0',
      'sec-fetch-user': '?1',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-dest': 'document'
    }

    return headers

def fiverrApiSearchRecommendation(term):
  r = requests.get(f'https://www.fiverr.com/recommendations/related_search_terms?search_term={term}', headers=random_headers())

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