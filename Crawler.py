# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import os
import time

def get_image(url, pic_name):
#chromedriver的路径
    chromedriver = r"C:\Users\cckuo\AppData\Local\Programs\Python\Python37-32\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
#设置chrome开启的模式，headless就是无界面模式
#一定要使用这个模式，不然截不了全页面，只能截到你电脑的高度
    chrome_options = Options()
    chrome_options.add_argument('headless')
    driver = webdriver.Chrome(chromedriver,chrome_options=chrome_options)
#控制浏览器写入并转到链接
    driver.get(url)
    time.sleep(1)
#接下来是全屏的关键，用js获取页面的宽高，如果有其他需要用js的部分也可以用这个方法

    width = driver.execute_script("return document.documentElement.scrollWidth")
    height = driver.execute_script("return document.documentElement.scrollHeight")
    print(width,height)
#将浏览器的宽高设置成刚刚获取的宽高
    # driver.set_window_size(width, height)
    driver.execute_script("document.body.style.zoom='1'")
    driver.set_window_size(4000, height)
    time.sleep(1)
#截图并关掉浏览器
    driver.save_screenshot(pic_name)
    driver.close()


# hea = {'User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}
# r = requests.get("https://bian.org/servicelandscape-8-0/views.html", headers = hea) #將網頁資料GET下來

url = 'https://bian.org/servicelandscape-8-0/views.html'
driver = webdriver.PhantomJS()
driver.get(url)
pageSource = driver.page_source
# print(pageSource)

soup = BeautifulSoup(pageSource,"lxml") #將網頁資料以html.parser
sels = soup.find_all('a', 'thumb') #div#section-contents-target div
print(len(sels))
# sels = sels[1:2]
# print(len(sels))

#webnames = ['view_31721','view_31853','view_27976']

i=1
for webname in sels:
    #抓檔案名稱
    filename = webname.find('div', 'diagram-title cutofftext').string.strip()
    url = 'https://bian.org/servicelandscape-8-0/%s' %webname['href']
    print(url)
    pic_name = r'D:\\爬蟲\\BIAN\\%s_%s.png' %(i,filename)
    print(pic_name)
    get_image(url, pic_name)
    i=i+1
