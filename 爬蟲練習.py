import requests
from bs4 import BeautifulSoup
from urllib import quote
import urlparse

search_list = []
keyword = quote('"柯文哲"'.encode('utf8'))
res = requests.get(
        "https://www.google.com.tw/search?num=50&q=" + keyword + "&oq=" + keyword + "&dcr=0&tbm=nws&source=lnt&tbs=qdr:d")

 # 關鍵字多加一個雙引號是精準搜尋
 # num: 一次最多要request的筆數, 可減少切換頁面的動作
 # tbs: 資料時間, hour(qdr:h), day(qdr:d), week(qdr:w), month(qdr:m), year(qdr:w)

if res.status_code == 200:
    content = res.content
    soup = BeautifulSoup(content, "html.parser")

    items = soup.findAll("div", {"class": "g"})
    for item in items:
        # title
        news_title = item.find("h3", {"class": "r"}).find("a").text

        # url
        href = item.find("h3", {"class": "r"}).find("a").get("href")
        parsed = urlparse.urlparse(href)
        news_link = urlparse.parse_qs(parsed.query)['q'][0]

        # content
        news_text = item.find("div", {"class": "st"}).text

        # source
        news_source = item.find("span", {"class": "f"}).text.split('-')
        news_from = news_source[0]
        time_created = str(news_source[1])

        # add item into json object
        search_list.append({
            "news_title": news_title,
            "news_link": news_link,
            "news_text": news_text,
            "news_from": news_from,
            "time_created": time_created
        })