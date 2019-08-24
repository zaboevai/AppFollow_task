from urllib import parse

from flask import request, Response

from app import app, db
from data_base.core import DataBase


@app.route('/posts/', methods=['GET'])
def index_page():
    news_db = DataBase(data_base=db)

    if request.method == 'GET':

        response = Response('', 404, content_type='text/plain')
        error = None
        default_query = {'offset': '0', 'limit': '5', 'order': None, 'order_desc': None}

        url = request.url
        parsed_url = parse.urlparse(url)
        user_query = parsed_url.query

        if user_query:
            error = parse_user_query(default_query, user_query)

            if error:
                response = Response(error, 404, content_type='text/html; charset="utf-8"')

        if not error:
            rows = news_db.get_json_rows_from_db(news_limit=default_query['limit'],
                                                 offset=default_query['offset'],
                                                 order_by=default_query['order'],
                                                 order_by_desc=default_query['order_desc'])

            if rows:
                response = Response(rows, 200,
                                    mimetype='application/json')

        return response

    return Response('', 404, content_type='text/plain')


# TODO reformat me
# TODO remake error handling via exceptions

def parse_user_query(default_query, user_query):
    error_text = None
    parsed_query = None
    errors = {'base': '<h3>Ошибка! Разрешенные запросы: limit, offset, order, order_desc.<br>' \
                      'Пример: http://localhost:8000/posts/?limit=10</h3>',
              'db': f"<h3>Для запроса {user_query} разрешены значения ('id','title','url','created')</h3>",
              'value': f"<h3>Для запроса {user_query} разрешены значения от 0 до 100</h3>", }
    try:
        parsed_query = dict(x.split('=') for x in user_query.split('&'))
    except ValueError as exc:
        error_text = errors['base']

    if parsed_query:
        for user_query, query_param in parsed_query.items():

            if not user_query in default_query:
                error_text = errors['base']
                break

            if user_query in ('order', 'order_desc'):
                if not query_param in ('id', 'title', 'url', 'created'):
                    error_text = errors['db']
                    break
            elif user_query in ('limit', 'offset'):
                try:
                    if not 0 <= int(query_param) <= 100:
                        error_text = errors['value']
                        break
                except ValueError:
                    error_text = errors['value']
                    break

            default_query[user_query] = query_param

    if error_text:
        return error_text

    return None
