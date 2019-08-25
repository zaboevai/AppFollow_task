import time
from threading import Thread
import requests

from app.models import News
from parsers.news import NEWS_TEST_DATA, HackerNews


class Parser(Thread):

    def __init__(self, data_base, url, news_count=0, sleep_time=0, test_mode=False, lock=None):
        super().__init__()
        self.url = url
        self.news_count = news_count
        self.test_mode = test_mode
        self.lock = lock
        self.inserted_count = 0
        self.sleep_time = sleep_time
        self.db = data_base

    def get_news(self, ):

        if self.test_mode:
            parsed_news = NEWS_TEST_DATA
        else:
            response = requests.get(url=self.url)
            parser = HackerNews(url=self.url, news_count=self.news_count)
            parser.feed(response.text)
            parsed_news = parser.get_news()
        return parsed_news

    def insert_news_to_db(self, db, parsed_news):
        with self.lock:
            self.inserted_count = db.insert(table=News, rows=parsed_news)

    def run(self):
        try:
            while True:
                parsed_news = self.get_news()
                self.insert_news_to_db(db=self.db, parsed_news=parsed_news)
                print(f'inserted: {self.inserted_count}')
                if self.sleep_time == 0:
                    break
                time.sleep(self.sleep_time)

        except BaseException as exc:
            raise exc
