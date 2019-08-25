from app import db


class News(db.Model):
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(256), nullable=False)
    url = db.Column(db.String(256), nullable=False)
    created = db.Column(db.DateTime, nullable=False)
