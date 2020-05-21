from bs4 import BeautifulSoup
import cssutils
import requests
import time
import json
from dateutil.parser import parse
# from .helpers import generate_article_url


class Punch(object):
    def __init__(self):
        self.url = 'http://punchng.com/'

    def get_topics(self):
        res = requests.get(self.url)
        html = BeautifulSoup(res.content, 'html.parser')
        if html:
            div = html.find('div', class_='menu-main-menu-container')

            ul = div.find('ul', class_='menu')

            lis = ul.find_all('li')
            topic_url = ul.find_all('a')
            topics = []
            for li in lis[1:]:
                topics.append(li.find('a').text.lower())
            return topics

    def get_topics_urls(self):
        res = requests.get(self.url)
        html = BeautifulSoup(res.content, 'html.parser')
        if html:
            div = html.find('div', class_='menu-main-menu-container')
            ul = div.find('ul', class_='menu')
            lis = ul.find_all('li')
            topics = {}
            for li in lis[1:]:
                topic = li.find('a').text.lower()
                topicUrl = li.find('a').get('href')
                topics[topic] = topicUrl
            return topics

    def get_article(self, topic, page):
        self.url = self.get_topics_urls()[topic.lower()] + 'page/' + str(page)
        print(self.url)
        res = requests.get(self.url)
        html = BeautifulSoup(res.content, 'html.parser')
        articles = []
        if html:
            div_cards = html.find('div', class_='cards no-gutter')
            divs = div_cards.find_all('div', class_='items col-sm-12')
            div_pagination = html.find('div', class_='paginations')
            page_anchors = div_pagination.find_all('a')

            total_pages = page_anchors[-1].text
            if "Next" in total_pages:
                total_pages = page_anchors[-2].text
            for divs in divs:
                articl_url = divs.find('a').get('href')
                article_title = divs.find('a').get('title')
                article_body = divs.find(
                    'div', class_='seg-summary').find('p').text
                article_publish_date = divs.find(
                    'div', class_='seg-time').find('span').text
                url = divs.find('div', class_='blurry')['style']
                style = cssutils.parseStyle(url)
                img_url = style['background-image']
                article_img_url = img_url.replace('url(', '').replace(')', '')
                article_content = []
                url_article = articl_url
                res = requests.get(url_article)
                html = BeautifulSoup(res.content, 'html.parser')
                div = html.find('div', class_='entry-content')
                # get only direct paragraph children
                p = div.find_all('p', recursive=False)

                for p in p:
                    for unnecessary_tag in p.find_all(['script', 'style', 'ins']):
                        unnecessary_tag.extract()
                    article_content.append(p.text)
                    # articles_content = ' '.join(article_content)

                    article = {
                        'publish_date': article_publish_date,
                        'title': article_title,
                        'url': articl_url,
                        'content': article_content,
                        'summary': article_body,
                        'url_to_article_image': article_img_url,

                    }
                    articles.append(article)
                # for article in articles:
                #     content = article.get('content')
                #     article['content'] = ' '.join(content)
        articles.append({'pages': total_pages})

        return articles

    def get_articles_by_date(self, topic, date, page=1):
        available_articles = self.get_article(topic, page)
        articles = []
        for article in available_articles:
            published_date = parse(article['publish_date']).timestamp()
            print(published_date)
            if published_date == date:
                articles.append(article)
        return articles


# punch = Punch()
# print(punch.get_articles('news'))
# print (punch.get_articles_by_date('news', 'April 6th, 2018'))

# print(punch.get_article_content("http://punchng.com/pcni-debunks-ty-danjumas-resignation-as-chairman/"))
