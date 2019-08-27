import time
from threading import Thread


class Parser(Thread):
    """
    Обработчик
    """
    def __init__(self, data_base, schema, sleep_time=0, lock=None):
        super().__init__()
        self.lock = lock
        self.inserted_count = 0
        self.sleep_time = sleep_time
        self.db = data_base
        self.parser_schema = schema

    def insert_news_to_db(self, parsed_news):
        """
        Вставка записей в БД
        :param parsed_news:     записи новостей
        :return:
        """
        with self.lock:
            self.inserted_count = self.db.insert(self.db.table_news, parsed_news)

    def start(self):
        """
        Разовый запуск процедуры
        :return:
        """
        parsed_news = self.parser_schema.get_news()
        self.insert_news_to_db(parsed_news=parsed_news)
        print(f'inserted: {self.inserted_count}')

    def run(self):
        """
        Периодический запуск с указанным интервалом
        :return:
        """
        try:
            while True:
                self.start()
                time.sleep(self.sleep_time)

        except BaseException as exc:
            raise exc
