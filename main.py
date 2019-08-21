import time
from html.parser import HTMLParser
import requests

from news_data_base import DataBase, News


SOURCE_URL = 'https://news.ycombinator.com'

# NEWS_TEMPLATE = [
#     {"id": 1,
#      "title": "Announcing Rust 1.33.0",
#      "url": "​https://example.com​ ",
#      "created": "ISO 8601"},
# ]

responce = requests.get(url=SOURCE_URL, )


# print(responce.text)


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


parser = NewsParser(url=SOURCE_URL)
parser.feed(responce.text)


NewsDB = DataBase()
NewsDB.create_db()
NewsDB.create_tables()

session = NewsDB.get_session()

for news in parser.get_news():
    session.add(News(**news))

session.commit()

s = session.query(News.id).filter(News.id == 1)
print(s.all())