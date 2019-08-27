import unittest
from urllib.parse import urljoin

import requests


class Api(unittest.TestCase):

    def setUp(self) -> None:
        self.localhost = 'http://0.0.0.0:8000'
        self.base_url = '/posts'
        field = 'title'
        cnt = 1
        self.querys = {'limit': f'limit={cnt}',
                       'offset': f'offset={cnt}',
                       'order': f'order={field}',
                       'order_desc': f'order_desc={field}',
                       }

    def test_connect(self):
        req = requests.get(self.localhost)
        self.assertFalse(req)

    def test_404_responce(self):
        req = requests.get(self.localhost)
        self.assertEqual(req.status_code, 404)

    def test_200_response(self):
        url = urljoin(self.localhost, self.base_url)
        req = requests.get(url)
        self.assertEqual(req.status_code, 200)

    def test_posts_json(self):
        url = urljoin(self.localhost, self.base_url)
        req = requests.get(url)
        self.assertEqual(req.headers['Content-Type'], 'application/json')

    def test_limit_json(self):
        url = urljoin(self.localhost, f"{self.base_url}/?{self.querys['limit']}")
        req = requests.get(url)
        self.assertEqual(req.headers['Content-Type'], 'application/json')

    def test_offset_json(self):
        url = urljoin(self.localhost, f"{self.base_url}/?{self.querys['offset']}")
        req = requests.get(url)
        self.assertEqual(req.headers['Content-Type'], 'application/json')

    def test_order_json(self):
        url = urljoin(self.localhost, f"{self.base_url}/?{self.querys['order']}")
        req = requests.get(url)
        self.assertEqual(req.headers['Content-Type'], 'application/json')

    def test_order_desc_json(self):
        url = urljoin(self.localhost, f"{self.base_url}/?{self.querys['order_desc']}")
        req = requests.get(url)
        self.assertEqual(req.headers['Content-Type'], 'application/json')

    def test_limit_offset_json(self):
        url = urljoin(self.localhost, f"{self.base_url}/?{self.querys['limit']}&{self.querys['offset']}")
        req = requests.get(url)
        self.assertEqual(req.headers['Content-Type'], 'application/json')

    def test_limit_offset_order_json(self):
        url = urljoin(self.localhost,
                      f"{self.base_url}/?{self.querys['limit']}&{self.querys['offset']}&{self.querys['order']}")
        req = requests.get(url)
        self.assertEqual(req.headers['Content-Type'], 'application/json')

    def test_limit_offset_order_desc_json(self):
        url = urljoin(self.localhost,
                      f"{self.base_url}/?{self.querys['limit']}&{self.querys['offset']}&{self.querys['order_desc']}")
        req = requests.get(url)
        self.assertEqual(req.headers['Content-Type'], 'application/json')
