from data_base.core import DataBase
from data_base.tables import News

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
# create db and table
NewsDB = DataBase()
NewsDB.create_db()
NewsDB.create_tables()
session = NewsDB.get_session()

# insert
NewsDB.insert(table=News, rows=NEWS_TEST_DATA)

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
