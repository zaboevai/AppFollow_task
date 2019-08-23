import json

import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

from data_base.news import Base, News


class DataBase:

    def __init__(self, engine_db=None):
        self.engine = engine_db
        self.session = None

    def create_db(self):
        self.engine = sqlalchemy.create_engine('sqlite:///news.db')
        self.create_tables()
        self.create_session()

    def create_tables(self):
        if not self.engine:
            raise BaseException('Создать таблицы не удалось, не определена БД')
        Base.metadata.create_all(self.engine)

    def create_session(self):
        if not self.engine:
            raise BaseException('Получить сессию не удалось, не определена БД')

        session_factory = sessionmaker(bind=self.engine)
        Session = scoped_session(session_factory)
        self.session = Session()
        # return self.session

    def get_session(self):
        return self.session

    def insert(self, table, rows):
        if not self.session:
            raise BaseException('Вставка невозможна, не удалось определить сессию')

        insert_count = 0
        for row in rows:
            if self.is_row_exist(table=table, row=row):
                # print('Row "{}" already exists'.format(str(row['title'])))
                continue
            row = table(**row)
            self.session.add(row)
            insert_count += 1
        self.session.commit()
        return insert_count

    def is_row_exist(self, table, row):
        row = self.session.query(table.id).filter(table.title == row['title'])
        for _ in row:
            return True
        return False

    def get_total_count_rows_from_db(self):
        total_rows = self.session.query(News).filter().count()
        return total_rows

    def get_json_rows_from_db(self):
        news_data = self.session.query(News).filter()
        rows = []
        for news in news_data:
            rows.append({'id': news.id,
                         'title': news.title,
                         'url': news.url,
                         'created': news.created.isoformat()
                         })

        json_rows = json.dumps(rows, indent=4)

        return json_rows
