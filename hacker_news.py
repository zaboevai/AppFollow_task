from threading import Lock

from app import app, db
from parser import NewsParser

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

    parser = NewsParser(url=SOURCE_URL,
                        data_base=db,
                        news_count=MAX_NEWS_COUNT,
                        sleep_time=10,
                        test_mode=False,
                        lock=lock)
    parser.start()
    app.run('localhost', 8000, debug=False)
    parser.join()


run()
