from app import app  # , SQLALCHEMY_DATABASE_URI


# from data_base.core import DataBase


@app.route('/posts', methods=['GET'])
def index_page():
    # news_db = DataBase(engine_db=SQLALCHEMY_DATABASE_URI)
    # news_db.create_session()
    rows = 'Hello'  # news_db.get_json_rows_from_db()

    if rows:
        response = (rows, '200 OK', [('Content-Type', 'text/plain')])
        return response

    return '', '404 Not Found', [('Content-Type', 'text/plain')]
