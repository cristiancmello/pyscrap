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

def chromeInit():
  uc.TARGET_VERSION = 85
  uc.install()

  from selenium.webdriver import Chrome
  from selenium.webdriver import Chrome, ChromeOptions

  opts = ChromeOptions()
  opts.add_argument('--no-sandbox')
  opts.add_argument('--disable-dev-shm-usage')
  opts.headless = False

  driver = Chrome(options=opts)
  return driver

driver = chromeInit()

def createDataFolder():
  folderName = 'data'
  if not os.path.exists(folderName):
    os.makedirs(folderName)

def saveSearchToFile(name, searchResult):
  filename = f'data/{name}.json'
  with open(filename, 'w', encoding='utf-8') as fp:
    js = json.dumps(searchResult, indent=2)
    fp.write(js)

def saveLog(name, data):
  filename = f'data/{name}.log'
  with open(filename, 'w', encoding='utf-8') as fp:
    fp.write(data)

def random_headers():
  headers = {
    'User-Agent': UserAgent().random,
    'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
    'upgrade-insecure-requests': '1',
    'sec-fetch-user': '?1',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-dest': 'document'
  }

  return headers

def fiverrApiSearchOmnibox(term, pro):
  r = requests.get(f'https://www.fiverr.com/search/layout/omnibox?callback=autocompleteCallback&from_medusa_header=true&pro_only={pro}&query={term}')
  saveLog('search_omnibox', r.text)
  return r.json()

def fiverrApiSearchRecommendation(term):
  r = requests.get(f'https://www.fiverr.com/recommendations/related_search_terms?search_term={term}', headers=random_headers())
  saveLog('search_recommendation', r.text)
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

def getCompetitionNumber(term):
  driver.get(f'https://www.fiverr.com/search/gigs?query={term}&source=top-bar&search_in=everywhere&search-autocomplete-original-term={term}')
  numberOfResultsElement = driver.find_element_by_xpath("//div[@class='number-of-results']")

  # Example: 12,123 Services => 12 and 123
  html_content = numberOfResultsElement.get_attribute('innerHTML')
  parsedTotalServiceList = re.findall(r'\d+', html_content)

  totalServicesString = ''

  for i in range(len(parsedTotalServiceList)):
    totalServicesString += parsedTotalServiceList[i]

  totalServiceInt = int(totalServicesString)

  return totalServiceInt

def getCompetitionRelationBySuggestions(suggestion_terms, type='basic', avoid_bot_detection=True, order_by='competition'):
  if type == 'basic':
    collectionName = 'suggestions'
    valueFieldName = 'value'
    orderFunction = orderCompetitionBasicRelation
  elif type == 'advanced':
    collectionName = 'related_search_terms'
    valueFieldName = 'query'
    orderFunction = orderCompetitionAdvancedRelation

  suggestions = suggestion_terms['data'][collectionName]

  for suggestion in suggestions:
    suggestion['competition'] = {
      'total': getCompetitionNumber(suggestion[valueFieldName]),
      'metadata': getSearchMetadata()
    }

    if avoid_bot_detection is True:
      time.sleep(random.random())
  
  suggestions = orderFunction(suggestions, order_by)

  return suggestions

def orderCompetitionBasicRelation(competition_relation, order_by='competition'):
  if order_by == 'competition':
    competition_relation = sorted(competition_relation, key = lambda i: i[order_by]['total'])
  else:
    raise Exception("Not implemented yet.")
  
  return competition_relation

def orderCompetitionAdvancedRelation(competition_relation, order_by='competition'):
  if order_by == 'competition':
    competition_relation = sorted(competition_relation, key = lambda i: i[order_by]['total'])
  elif order_by == 'pos':
    None
  else:
    raise Exception("Not implemented yet.")
  
  return competition_relation

def generateCompetitionRelation(term, type='basic', save_to_file=True):
  if type == 'basic':
    searchRecommendations = searchBasicRecommendations(term)
  else:
    searchRecommendations = searchAdvancedRecomendations(term)

  competitionRelation = getCompetitionRelationBySuggestions(
    suggestion_terms=searchRecommendations, 
    type=type, 
    avoid_bot_detection=True, 
    order_by='competition'
  )

  if save_to_file is True:
    saveSearchToFile(f'{type}_search_{term}', searchRecommendations)
    saveSearchToFile(f'{type}_competition_relation_{term}', competitionRelation)

def main():
  createDataFolder()

  generateCompetitionRelation('php', 'basic')
  driver.quit()

main()