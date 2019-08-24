import json
from app.models import News


class DataBase:

    def __init__(self, data_base):
        self.db = data_base

    def insert(self, table, rows):
        if not self.db.session:
            raise BaseException('Вставка невозможна, не удалось определить сессию')

        insert_count = 0
        for row in rows:
            if self.is_row_exist(table=table, row=row):
                # print('Row "{}" already exists'.format(str(row['title'])))
                continue
            row = table(**row)
            self.db.session.add(row)
            insert_count += 1
        self.db.session.commit()
        return insert_count

    def is_row_exist(self, table, row):
        row = self.db.session.query(table.id).filter(table.title == row['title'])
        for _ in row:
            return True
        return False

    def get_total_count_rows_from_db(self):
        total_rows = self.db.session.query(News).filter().count()
        return total_rows

    def get_json_rows_from_db(self, news_limit=None, offset=None, order_by=None, order_by_desc=None):
        if not self.db.session:
            raise BaseException('Вставка невозможна, не удалось определить сессию')

        news_data = self.db.session.query(News).order_by(News.created.desc()).offset(offset).limit(news_limit)

        if order_by_desc:
            if order_by_desc == 'title':
                news_data = news_data.from_self().order_by(News.title.desc()).all()
            elif order_by_desc == 'created':
                news_data = news_data.from_self().order_by(News.created.desc()).all()
            elif order_by_desc == 'url':
                news_data = news_data.from_self().order_by(News.url.desc()).all()
            elif order_by_desc == 'id':
                news_data = news_data.from_self().order_by(News.id.desc()).all()
        else:
            if order_by == 'title':
                news_data = news_data.from_self().order_by(News.title).all()
            elif order_by == 'created':
                news_data = news_data.from_self().order_by(News.created).all()
            elif order_by == 'url':
                news_data = news_data.from_self().order_by(News.url).all()
            elif order_by == 'id':
                news_data = news_data.from_self().order_by(News.id).all()

        rows = []
        news_id = 0
        for news in news_data:
            news_id += 1
            rows.append({'id': news_id,
                         'title': news.title,
                         'url': news.url,
                         'created': news.created.isoformat(" ", "seconds")
                         })

        json_rows = json.dumps(rows, indent=4)

        return json_rows
