import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class News(Base):
    __tablename__ = 'news'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
    title = sqlalchemy.Column(sqlalchemy.String(256), nullable=False)
    url = sqlalchemy.Column(sqlalchemy.String(256), nullable=False)
    created = sqlalchemy.Column(sqlalchemy.String(256), nullable=False)
