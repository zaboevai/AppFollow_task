import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from data_base.core import DataBase

app = Flask(__name__)


@app.route('/posts', methods=['GET'])
def index_page():
    news_db = DataBase()
    news_db.create_db()
    rows = news_db.get_json_rows_from_db()

    if rows:
        response = (rows, '200 OK', [('Content-Type', 'text/plain')])
        return response

    return '', '404 Not Found', [('Content-Type', 'text/plain')]


def run_api(debug=False):
    app.run('localhost', 8000, debug=debug)
