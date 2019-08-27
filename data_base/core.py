import json


class DataBase:
    """
    Клас для работы с БД
    """
    def __init__(self, data_base):
        self.db = data_base
        try:
            from app.models import News
            self.table_news = News
        except ImportError:
            raise ImportError

    def insert(self, table, rows):
        """
        Вставка в таблицу БД
        :param table:   таблица
        :param rows:    записи
        :return:        кол-во вставленных записей
        """
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
        """
        Проверка перед вставкой на наличие записи в БД по полю "title"
        :param table:   таблица
        :param row:     запись
        :return:        результат true - если запись есть в БД
        """
        row = self.db.session.query(table.id).filter(table.title == row['title'])
        for _ in row:
            return True
        return False

    def get_total_count_rows_from_db(self, table):
        """
        Возвращает общее кол-во записей в таблице
        :param table:   таблица
        :return:        кол-во записей
        """
        total_rows = self.db.session.query(table).filter().count()
        return total_rows

    def get_rows_from_db(self, limit=None, offset=None, order_by=None, order_by_desc=None):
        """
        Возвращает записи из БД в зависимости от параметров
        :param limit:           кол-во записей
        :param offset:          сдвиг записей
        :param order_by:        сортировка
        :param order_by_desc:   сортировка с конца
        :return:                записи
        """
        if not self.db.session:
            raise BaseException('Вставка невозможна, не удалось определить сессию')

        total_limit = int(limit)+int(offset)

        news_data = self.db.session.query(self.table_news).order_by(self.table_news.created.desc()).limit(total_limit)

        if order_by_desc:
            if order_by_desc == 'title':
                news_data = news_data.from_self().order_by(self.table_news.title.desc()).offset(offset).limit(limit)
            elif order_by_desc == 'created':
                news_data = news_data.from_self().order_by(self.table_news.created.desc()).offset(offset).limit(limit)
            elif order_by_desc == 'url':
                news_data = news_data.from_self().order_by(self.table_news.url.desc()).offset(offset).limit(limit)
            else:
                news_data = news_data.from_self().order_by(self.table_news.id.desc()).offset(offset).limit(limit)

        elif order_by:

            if order_by == 'title':
                news_data = news_data.from_self().order_by(self.table_news.title).offset(offset).limit(limit)
            elif order_by == 'created':
                news_data = news_data.from_self().order_by(self.table_news.created).offset(offset).limit(limit)
            elif order_by == 'url':
                news_data = news_data.from_self().order_by(self.table_news.url).offset(offset).limit(limit)
            else:
                news_data = news_data.from_self().order_by(self.table_news.id).offset(offset).limit(limit)
        else:
            news_data = news_data.from_self().offset(offset).limit(limit)

        return news_data

    @staticmethod
    def convert_news_to_json(news_data):
        """
        Конвертирует записи новостей в json формат
        :param news_data:  записи новостей для конвертации
        :return:           записи в json
        """
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
