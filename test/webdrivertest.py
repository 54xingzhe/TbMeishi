from time import sleep
from selenium import webdriver

browser = webdriver.Chrome()
browser.get('https://www.taobao.com')
sleep(10)
browser.close()
