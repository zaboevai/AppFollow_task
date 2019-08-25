from threading import Lock

from app import app, db
from data_base.core import DataBase
from parsers.core import Parser

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
    news_db = DataBase(data_base=db)
    news_parser = Parser(url=SOURCE_URL,
                         data_base=news_db,
                         news_count=MAX_NEWS_COUNT,
                         sleep_time=10,
                         test_mode=False,
                         lock=lock)
    news_parser.start()
    app.run('localhost', 8000, debug=True)
    news_parser.join()


if __name__ == '__main__':
    run()
