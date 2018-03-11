import re
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By  # 元素定位，加载目标
from selenium.webdriver.support.ui import WebDriverWait  # 等待页面加载完成，找到某个条件发生后再继续执行后续代码，如果超过设置时间检测不到则抛出异常
from selenium.webdriver.support import expected_conditions as EC  # 选择条件
from pyquery import PyQuery as pq
from config import *
import pymongo

# 声明MongoDB的链接信息
client = pymongo.MongoClient(MONGO_URL)
db = client[MONGO_DB]

# browser = webdriver.Chrome()  # 先使用Chrome浏览器，Chrome()浏览器调试方便，然后再改phantomJS
browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)  # 使用无界面浏览器，在后台运行
wait = WebDriverWait(browser, 10)  # 设置最长等待时间

browser.set_window_size(1400, 900)  # 窗口大小


def search():
    '''定义搜索方法'''
    print('正在搜索')
    try:
        browser.get('https://www.taobao.com')  # 用get方法请求淘宝首页
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#q'))
        )  # 输入框  presence_of_element_located()判断元素是否存在页面中
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '#J_TSearchForm > div.search-button > button'))
        )  # 提交按钮
        input.send_keys(KEYWORD)  # 输入搜索关键字
        submit.click()  # 点击搜索按钮
        total = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.total'))
        )  # 获取总页数
        get_products()  # 页面打开后，调用解析方法
        return total.text  # 返回页数（返回的是标签里的内容）
    except TimeoutException:  # 使用父类异常
        return search()  # 如果出现错误，重新请求一次

def next_page(page_number):
    '''定义获取下一页方法'''
    print('正在翻页', page_number)
    try:
        input = wait.until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > input')
            )
        )  # 输入页数
        submit = wait.until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit')
            )
        )  # 提交按钮
        input.clear()  # 先清除原来页码
        input.send_keys(page_number)  # 输入页码
        submit.click()  # 提交按钮
        wait.until(
            EC.text_to_be_present_in_element(
                (By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(page_number)
            )
        )  # text_to_be_present_in_element() 判断在这个元素里面是否有这样的文字，从而判断是否翻页成功
        get_products()  # 判断翻页成功后，调用解析方法
    except TimeoutException:
        next_page(page_number)  # 如果出错，重新请求一次，实现递归

def get_products():
    '''定义解析的方法'''
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#mainsrp-itemlist .items .item'))
    )  # 获取每个商品的div
    html = browser.page_source  # 获取到网页源代码
    doc = pq(html)  # 用pyquery解析
    items = doc('#mainsrp-itemlist .items .item').items()  # 得到所有选择内容
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text()[:-3],  # 成交量
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        save_to_mongo(product)  # 拿到数据后，保存到库

def save_to_mongo(result):
    '''定义存储数据库的方法'''
    try:
        if db[MONGO_TABLE].insert(result):  # 如果保存成功，打印出来
            print('存储到MONGODB成功', result)
    except Exception:
        print('存储到MONGO失败', result)

def main():
    try:
        total = search()
        total = int(re.compile('(\d+)').search(total).group(1))  # 用正则获取总页数数字
        # print(total)
        for i in range(2, total + 1):  # 用range()方法实现页码循环，刚打开是第一页，从第二页开始翻页
            next_page(i)
    except Exception:
        print('出错了')
    finally:
        browser.close()  # 关闭浏览器


if __name__ == '__main__':
    main()
