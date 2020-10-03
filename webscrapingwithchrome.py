import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service



from selenium import webdriver
from selenium.webdriver.chrome.options import Options

chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')

browser = webdriver.Chrome(chrome_options=chrome_options)

driver.get('http://www.google.com/');

time.sleep(5)

driver.quit()