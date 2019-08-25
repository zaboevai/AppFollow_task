from urllib import parse
from flask import request, Response

from app import app, news_db

DEFAULT_QUERY = {'offset': '0', 'limit': '5', 'order': None, 'order_desc': None}


@app.route('/posts/', methods=['GET'])
def index_page():
    if request.method == 'GET':

        url = request.url
        parsed_url = parse.urlparse(url)
        user_query = parsed_url.query

        if user_query:
            parsed_query, error = parse_user_query(user_query)

            if error:
                return Response(error, 404, content_type='text/html; charset="utf-8"')
        else:
            parsed_query = DEFAULT_QUERY

        rows = news_db.get_rows_from_db(limit=parsed_query['limit'],
                                        offset=parsed_query['offset'],
                                        order_by=parsed_query['order'],
                                        order_by_desc=parsed_query['order_desc'])

        json_rows = news_db.conver_to_json(rows)

        if rows:
            return Response(json_rows, 200, mimetype='application/json')

    return Response('', 404, content_type='text/plain')


# TODO reformat me
# TODO remake error handling via exceptions

def parse_user_query(user_query):
    error_text = None
    parsed_query = {}
    result_query = {}
    errors = {'base': '<h3>Ошибка! Разрешенные запросы: limit, offset, order, order_desc.<br>' \
                      'Пример: http://localhost:8000/posts/?limit=10</h3>',
              'db': f"<h3>Для запроса {user_query} разрешены значения ('id','title','url','created')</h3>",
              'value': f"<h3>Для запроса {user_query} разрешены значения от 0 до 100</h3>", }
    try:
        parsed_query = dict(x.split('=') for x in user_query.split('&'))
    except ValueError:
        error_text = errors['base']

    if parsed_query:
        result_query = DEFAULT_QUERY.copy()
        for user_query, query_param in parsed_query.items():

            if user_query not in DEFAULT_QUERY:
                error_text = errors['base']
                break

            if user_query in ('order', 'order_desc'):
                if query_param not in ('id', 'title', 'url', 'created'):
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

            result_query[user_query] = query_param

    return result_query, error_text
