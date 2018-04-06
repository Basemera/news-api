from bs4 import BeautifulSoup
import requests
import time
import json
from dateutil.parser import parse

class Punch(object):
    def __init__(self):
        self.url = "http://punchng.com/"
        
    def getTopics(self):
        res = requests.get(self.url)
        html = BeautifulSoup(res.content, 'html.parser')
        if html:
            div = html.find('div', class_="menu-main-menu-container")
            ul = div.find('ul', class_='menu')
            lis = ul.find_all('li')
            topics = []
            for li in lis[1:]:
                topics.append(li.find('a').text.lower())
            return topics

    def getTopicUrls(self):
        res = requests.get(self.url)
        html = BeautifulSoup(res.content, 'html.parser')
        if html:
            div = html.find('div', class_="menu-main-menu-container")
            ul = div.find('ul', class_='menu')
            lis = ul.find_all('li')
            topics = {}
            for li in lis[1:]:
                topic = li.find('a').text.lower()
                topicUrl = li.find('a').get('href')
                topics[topic] = topicUrl
            return topics

    def getArticles(self, topic):
        self.url = self.getTopicUrls()[topic.lower()]
        res = requests.get(self.url)
        html = BeautifulSoup(res.content, 'html.parser')
        articles = []
        if html:
            main = html.find('main', class_="site-main container-fluid")
            section = main.find('section', class_="row .lll")
            div_cards = section.find('div', class_="cards no-gutter")
            divs = div_cards.find_all('div', class_='items col-sm-12')
            for divs in divs:
                articleUrl = divs.find('a').get('href')
                articleTitle = divs.find('a').get('title')
                article_body = divs.find('div', class_='seg-summary').find('p').text
                article_publish_date = divs.find('div', class_="seg-time").find('span').text
                article = {
                    'url':articleUrl,
                    'title':articleTitle,
                    'body': article_body,
                    'publish date':article_publish_date
                }
                articles.append(article)
        return articles

    def get_articles_by_date(self, topic, date):
        available_articles = self.getArticles(topic)
        articles = []
        for article in available_articles:
            published_date = parse(article['publish date']).timestamp()
            if published_date == date:
                articles.append(article)
        return articles

# punch = Punch()
# print (punch.get_articles_by_date('news', 'April 6th, 2018'))
                

