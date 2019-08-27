import urllib
from abc import ABC
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

import requests

NEWS_TEST_DATA = [
    {"title": "title_1123",
     "url": "https://example.com",
     "created": datetime.today()
     },

    {"title": "title_2",
     "url": "https://example.com",
     "created": datetime.today()
     },

    {"title": "title_3",
     "url": "https://example.com",
     "created": datetime.today()
     },

    {"title": "title_4",
     "url": "https://example.com",
     "created": datetime.today()
     },
]


class HackerNewsHandler(HTMLParser, ABC):
    """
    Обработчик новостей с сайта hacker news
    """
    def __init__(self, url, news_count=0):
        super().__init__()
        self.url = url
        self.news_count = news_count
        self.one_news = {}
        self.news = []
        self.is_find = False

    def handle_starttag(self, tag, attrs):
        """
        Обработка начала тега html страницы
        :param tag:
        :param attrs:
        :return:
        """
        if self.news_count == len(self.news):
            return

        attrs = dict(attrs)
        if not (tag == 'a' and 'storylink' in attrs.values()):
            return

        self.one_news.clear()
        self.is_find = True

        url_scheme = urlparse(attrs['href'])[0]
        if not url_scheme:
            base_url = self.url.split('/news?')[0]
            self.one_news['url'] = urljoin(base=base_url, url=attrs['href'])
        else:
            self.one_news['url'] = attrs['href']

    def handle_data(self, data):
        """
        Обработка тела тега html страницы
        :param data:
        :return:
        """
        if self.is_find:
            self.one_news['title'] = data
            self.one_news['created'] = datetime.today()

    def handle_endtag(self, tag):
        """
        Обработка конца тега html страницы
        :param tag:
        :return:
        """
        if self.is_find:
            news = self.one_news.copy()
            self.news.append(news)
            self.is_find = False

    def get_news(self):
        """
        Возвращает найденные новости со страницы сайта
        :return:
        """
        response = requests.get(url=self.url)
        self.feed(response.text)
        return self.news
