import unittest
from unittest.mock import Mock

from hacker_news import NewsParser


class HackerNewsTest(unittest.TestCase):

    def setUp(self):
        db = Mock()
        lock = Mock()
        self.parser = Mock()
        SOURCE_URL = 'https://news.ycombinator.com'
        MAX_NEWS_COUNT = 30
        self.parser = NewsParser(url=SOURCE_URL,
                                 news_count=MAX_NEWS_COUNT,
                                 sleep_time=10,
                                 test_mode=False,
                                 lock=lock)

    def test_start(self):
        self.parser.run_news_parser()
