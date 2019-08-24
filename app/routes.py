from urllib import parse

from flask import request, Response

from app import app, db
from data_base.core import DataBase


@app.route('/posts/', methods=['GET'])
def index_page():
    news_db = DataBase(data_base=db)

    if request.method == 'GET':

        default_query = {'offset': '0', 'limit': '5', 'order': None, 'order_desc': None}

        url = request.url
        parsed_url = parse.urlparse(url)
        query = parsed_url.query

        if query:
            try:
                parsed_query = dict(x.split('=') for x in query.split('&'))
            except ValueError as exc:
                error_text = '<h3>Ошибка! Разрешенные запросы: limit, offset, order, order_desc.<br>' \
                             'Пример: http://localhost:8000/posts/?limit=10</h3>'
                return Response(error_text, 404, content_type='text/html; charset="utf-8"')

            for query, query_param in parsed_query.items():
                if query in ('order', 'order_desc'):
                    if not query_param in ('id', 'title', 'url', 'created'):
                        error_text = f"<h3>Для запроса {query} разрешены значения ('id','title','url','created')</h3>"

                        return Response(error_text, 404, content_type='text/html; charset="utf-8"')
                elif query in ('limit', 'offset'):

                    if not 0 <= int(query_param) <= 100:
                        error_text = f"<h3>Для запроса {query} разрешены значения от 0 до 100</h3>"
                        return Response(error_text, 404, content_type='text/html; charset="utf-8"')

                if not query in default_query:
                    error_text = f"<h3>Для запроса {query} разрешены значения от 0 до 100</h3>"
                    return Response(error_text, 404, content_type='text/html; charset="utf-8"')

                default_query[query] = query_param

        rows = news_db.get_json_rows_from_db(news_limit=default_query['limit'],
                                             offset=default_query['offset'],
                                             order_by=default_query['order'],
                                             order_by_desc=default_query['order_desc'])
        # else:
        #     rows = news_db.get_json_rows_from_db()

        if rows:
            response = Response(rows, 200,
                                mimetype='application/json')  # content_type='text/plain')  # (rows, '200 OK', [('Content-Type', 'text/plain')])
            return response

    return Response('', 404, content_type='text/plain')
