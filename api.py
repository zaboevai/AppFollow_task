from flask import Flask
from data_base.core import get_json_rows_from_db

app = Flask(__name__)


@app.route('/posts', methods=['GET'])
def index_page():
    rows = get_json_rows_from_db()
    response = (rows, '200 OK', [('Content-Type', 'text/plain')])
    return response


def run_api():
    app.run('localhost', 8000, debug=True)
