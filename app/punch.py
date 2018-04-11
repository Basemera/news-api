from bs4 import BeautifulSoup
import cssutils
import requests
import time
import json
from dateutil.parser import parse
from .helpers import generate_article_url

class Punch(object):
    def __init__(self):
        self.url = "http://punchng.com/"
        
    def get_topics(self):
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

    def get_topics_urls(self):
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

    def get_articles(self, topic):
        self.url = self.get_topics_urls()[topic.lower()]
        res = requests.get(self.url)
        html = BeautifulSoup(res.content, 'html.parser')
        articles = []
        if html:
            main = html.find('main', class_="site-main container-fluid")
            section = main.find('section', class_="row .lll")
            div_cards = section.find('div', class_="cards no-gutter")
            divs = div_cards.find_all('div', class_='items col-sm-12')
            pagination_section = main.find('section', class_="first-row")
            div_pagination = pagination_section.find('div', class_="paginations")
            a = div_pagination.find_all('a')
            total_pages = []
            for a in a:
                total_pages.append(a.text)
            for divs in divs:
                articleUrl = divs.find('a').get('href')
                articleTitle = divs.find('a').get('title')
                article_body = divs.find('div', class_='seg-summary').find('p').text
                article_publish_date = divs.find('div', class_="seg-time").find('span').text
                article_content = self.get_article_content(articleUrl)
                url = divs.find('div', class_="blurry")['style']
                style = cssutils.parseStyle(url)
                img_url = style['background-image']
                article_img_url = img_url.replace('url(', '').replace(')', '')
                
                article = {
                    'publish_date':article_publish_date,
                    'title':articleTitle,
                    'url':articleUrl,
                    'content':article_content,
                    'summary': article_body,
                    'url_to_article_image':article_img_url
                    
                }
                articles.append(article)
            articles.append(total_pages)
        return articles

    def get_article_content(self, url):
        article_content = []
        self.url = url
        res = requests.get(self.url)
        html = BeautifulSoup(res.content, 'html.parser')
        div = html.find('div', class_="entry-content")
       # get only direct paragraph children
        p = div.find_all('p', recursive=False)

        for p in p:
            for unnecessary_tag in p.find_all(['script', 'style', 'ins']):
                unnecessary_tag.extract()
            article_content.append(p.text)
        return article_content

    def get_articles_by_date(self, topic, date):
        available_articles = self.get_articles(topic)
        articles = []
        for article in available_articles:
            published_date = parse(article['publish_date']).timestamp()
            if published_date == date:
                articles.append(article)
        return articles

punch = Punch()
# print(punch.get_articles('news'))
# print (punch.get_articles_by_date('news', 'April 6th, 2018'))
                
# print(punch.get_article_content("http://punchng.com/pcni-debunks-ty-danjumas-resignation-as-chairman/"))
