"""Tests for logic to look up individual article metdata.

License: BSD
"""

import unittest

import article_getter


class ArticleGetterTests(unittest.TestCase):

    def test_article_to_dict(self):
        article = article_getter.Article(
            'test url',
            'title original',
            'title english',
            '2024-01-17',
            'us',
            ['keyword'],
            ['tags'],
            ['categories']
        )
        target_dict = article.to_dict()
        self.assertEqual(target_dict['url'], 'test url')

    def test_local_handler_all(self):
        results = article_getter.local_handler({})
        self.assertTrue(len(results) > 0)
        self.assertTrue(results[0].get_url() != '')

    def test_local_handler_filter(self):
        results = article_getter.local_handler({'keyword': 'security'})
        self.assertTrue(len(results) > 0)
        self.assertTrue(results[0].get_url() != '')
