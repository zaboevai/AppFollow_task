from app import app, db
from data_base.core import DataBase


@app.route('/posts', methods=['GET'])
def index_page():
    news_db = DataBase(data_base=db)
    rows = news_db.get_json_rows_from_db()

    if rows:
        response = (rows, '200 OK', [('Content-Type', 'text/plain')])
        return response

    return '', '404 Not Found', [('Content-Type', 'text/plain')]
