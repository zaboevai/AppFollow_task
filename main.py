from data_base.core import get_db
from data_base.tables import News
from parser import get_news_from_url

SOURCE_URL = 'https://news.ycombinator.com'

NEWS_TEST_DATA = [
    {"title": "title_1",
     "url": "https://example.com",
     "created": "ISO 8601"},

    {"title": "title_2",
     "url": "https://example.com",
     "created": "ISO 8601"},

    {"title": "title_3",
     "url": "https://example.com",
     "created": "ISO 8601"},

    {"title": "title_4",
     "url": "https://example.com",
     "created": "ISO 8601"},
]


def run_news_parser(url, test_mode=False):
    if test_mode:
        parsed_news = NEWS_TEST_DATA
    else:
        parsed_news = get_news_from_url(url=url, news_count=2)

    news_db, session = get_db()
    news_db.insert(table=News, rows=parsed_news)

    # select
    news_data = session.query(News).filter()
    for news in news_data:
        print(news.id, news.title, news.url, news.created)

"""
decompose task:

NewsParser:
1) create table (if needed)
2) get_news
3) insert news into table
4) update data

API
1) parse request
2) get data from table
3) sorting (if needed)
4) send response

"""

run_news_parser(url=SOURCE_URL, test_mode=True)
