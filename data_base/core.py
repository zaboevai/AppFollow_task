import sqlalchemy
from sqlalchemy.orm import sessionmaker, scoped_session

from data_base.tables import Base


class DataBase:

    def __init__(self):
        self.engine = None
        self.session = None

    def create_db(self):
        self.engine = sqlalchemy.create_engine('sqlite:///news.db')

    def create_tables(self):
        if self.engine:
            Base.metadata.create_all(self.engine)

    def get_session(self):
        session_factory = sessionmaker(bind=self.engine)
        Session = scoped_session(session_factory)
        self.session = Session()
        return self.session

    def insert(self, table, rows):

        for row in rows:
            if self.is_row_exist(table=table, row=row):
                continue
            row = table(**row)
            session.add(row)
        session.commit()

    def is_row_exist(self, table, row):
        row = self.session.query(table).filter(table.title == row['title'])
        for data in row:
            return True
            break
        return False


# if __name__ == '__MAIN__':
NewsDB = DataBase()
NewsDB.create_db()
NewsDB.create_tables()

session = NewsDB.get_session()
