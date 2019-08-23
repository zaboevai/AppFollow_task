import time
from abc import ABC
from datetime import datetime
from html.parser import HTMLParser
from threading import Thread
from urllib.parse import urlparse, urljoin

import requests

from data_base.core import get_db
from data_base.news import News

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


class HackerNewsParser(HTMLParser, ABC):

    def __init__(self, base_url, news_count=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_find = False
        self.news_count = news_count
        self.fresh_news = []
        self.news = {}
        self.base_url = base_url
        self.is_find = False

    def handle_starttag(self, tag, attrs):

        if self.news_count == len(self.fresh_news):
            return

        attrs = dict(attrs)
        if not (tag == 'a' and 'storylink' in attrs.values()):
            return

        self.news.clear()
        self.is_find = True

        url_scheme = urlparse(attrs['href'])[0]
        if not url_scheme:
            self.news['url'] = urljoin(base=self.base_url, url=attrs['href'])
        else:
            self.news['url'] = attrs['href']

    def handle_data(self, data):
        if self.is_find:
            self.news['title'] = data
            self.news['created'] = datetime.today()

    def handle_endtag(self, tag):
        if self.is_find:
            news = self.news.copy()
            self.fresh_news.append(news)
            self.is_find = False

    def get_news(self):
        return self.fresh_news


def get_news_from_url(url, news_count=0):
    response = requests.get(url=url, )
    base_url = url.split('/news?')[0]

    parser = HackerNewsParser(base_url=base_url, news_count=news_count)
    parser.feed(response.text)

    return parser.get_news()


class NewsParser(Thread):

    def __init__(self, url, news_count=0, sleep_time=0, test_mode=False, lock=None):
        super().__init__()
        self.url = url
        self.news_count = news_count
        self.test_mode = test_mode
        self.news_db, self.session = get_db()
        self.lock = lock
        self.inserted_count = 0
        self.sleep_time = sleep_time

    def run_news_parser(self, ):

        if self.test_mode:
            parsed_news = NEWS_TEST_DATA
        else:
            parsed_news = get_news_from_url(url=self.url, news_count=self.news_count)

        with self.lock:
            self.inserted_count = self.news_db.insert(table=News, rows=parsed_news)

    def get_total_count_rows_from_db(self):
        total_rows = self.session.query(News).filter().count()
        return total_rows

    def run(self):

        try:
            while True:

                # print(f'before : {self.get_total_count_rows_from_db()}')
                self.run_news_parser()
                print(f'inserted: {self.inserted_count}')
                # print(f'after: {self.get_total_count_rows_from_db()}')
                if self.sleep_time == 0:
                    break

                time.sleep(self.sleep_time)

        except BaseException as exc:
            raise exc
