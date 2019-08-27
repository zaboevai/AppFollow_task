import time
from threading import Thread


class Parser(Thread):

    def __init__(self, data_base, schema, sleep_time=0, lock=None):
        super().__init__()
        self.lock = lock
        self.inserted_count = 0
        self.sleep_time = sleep_time
        self.db = data_base
        self.parser_schema = schema

    def insert_news_to_db(self, parsed_news):
        with self.lock:
            self.inserted_count = self.db.insert(self.db.table_news, parsed_news)

    def start(self):
        parsed_news = self.parser_schema.get_news()
        self.insert_news_to_db(parsed_news=parsed_news)
        print(f'inserted: {self.inserted_count}')

    def run(self):
        try:
            while True:
                self.start()
                time.sleep(self.sleep_time)

        except BaseException as exc:
            raise exc
