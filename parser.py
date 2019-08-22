import time
from html.parser import HTMLParser

import requests


class NewsParser(HTMLParser):

    def __init__(self, url, news_count=5, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_find = False
        self.fresh_news = []
        self.news = {}
        self.count = 1

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)

        if not (tag == 'a' and 'storylink' in attrs.values()):
            self.is_find = False
            return

        self.news.clear()
        self.is_find = True
        self.news['id'] = len(self.fresh_news) + 1
        self.news['url'] = attrs['href']

    def handle_endtag(self, tag):
        if self.is_find:
            news = self.news.copy()
            self.fresh_news.append(news)
            # print(self.news)

    def handle_data(self, data):
        if self.is_find:
            self.news['title'] = data
            self.news['created'] = time.localtime()

    def get_news(self):
        return self.fresh_news


def get_news_from_url(url, news_count=0):
    response = requests.get(url=url, )
    parser = HackerNewsParser(news_count=news_count)
    parser.feed(response.text)
    return parser.get_news()
