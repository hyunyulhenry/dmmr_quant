import requests as rq
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from bs4 import BeautifulSoup

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

url = 'https://edition.cnn.com/markets/fear-and-greed'
driver.get(url)

html = driver.page_source
bs = BeautifulSoup(html)

bs.select('div.market-fng-gauge__dial-number > span.market-fng-gauge__dial-number-value')[0].get_text()
