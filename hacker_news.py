from threading import Lock

from app import app, news_db
from parsers.core import Parser
from parsers.news import HackerNews

SOURCE_URL = 'https://news.ycombinator.com'

MAX_NEWS_COUNT = 30

"""
decompose task:

NewsParser:
1) create table (if needed)
2) get_news
3) insert news into table


API
1) parse request
2) get data from table
3) sorting (if needed)
4) send response

"""


def run():
    lock = Lock()
    news_parser = Parser(url=SOURCE_URL,
                         data_base=news_db,
                         schema=HackerNews,
                         news_count=MAX_NEWS_COUNT,
                         sleep_time=3600,
                         test_mode=False,
                         lock=lock)
    news_parser.start()
    news_parser.join()


if __name__ == '__main__':
    run()
