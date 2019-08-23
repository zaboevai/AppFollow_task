from threading import Thread

from api import run_api
from parser import run_news_parser

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
    run_news_parser(url=SOURCE_URL, news_count=MAX_NEWS_COUNT, test_mode=False)

    run_api()
    # print(get_rows_from_db())


run()
