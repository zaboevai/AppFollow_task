from abc import ABC
from datetime import datetime
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin

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


class HackerNews(HTMLParser, ABC):

    def __init__(self, url, news_count=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_find = False
        self.news_count = news_count
        self.fresh_news = []
        self.news = {}
        self.url = url
        self.base_url = url.split('/news?')[0]
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


