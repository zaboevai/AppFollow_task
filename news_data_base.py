import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(256), nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String(256), nullable=False)
    created = sqlalchemy.Column(sqlalchemy.Text, nullable=False)


class DataBase:
    def __init__(self):
        self.engine = None
        self.session = None

    def create_db(self):
        self.engine = sqlalchemy.create_engine('sqlite:///news.db')
        Base.metadata.create_all(self.engine)
        # self.session = create_session(engine)

    def create_tables(self):
        if self.engine:
            Base.metadata.create_all(self.engine)

    def get_session(self):
        session_factory = sessionmaker(bind=self.engine)
        Session = scoped_session(session_factory)
        self.session = Session()
        return self.session


if __name__ == '__MAIN__':
    NewsDB = DataBase()
    NewsDB.create_db()
    NewsDB.create_tables()

    session = NewsDB.get_session()
