from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pyquery import PyQuery as pq

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 10)
browser.get('https://www.taobao.com')

input = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#q')))
submit = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button')))
input.send_keys('美食')
submit.click()

html = browser.page_source
# print(html)

doc = pq(html)
items = doc('#mainsrp-itemlist .items .item').items()
print(items)

for item in items:
    product = {
        'image': item.find('.pic .img').attr('src'),
        'price': item.find('.price').text(),
        'deal': item.find('.deal-cnt').text()[:-3],
        'title': item.find('.title').text(),
        'shop': item.find('.shop').text(),
        'location': item.find('.location').text()
    }
    print(product)
