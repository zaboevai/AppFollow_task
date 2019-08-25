from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from data_base.core import DataBase


app = Flask(__name__)

app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

news_db = DataBase(data_base=db)

from app import routes, models
