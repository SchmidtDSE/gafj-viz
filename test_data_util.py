"""Tests for utilities to query for aggregate statistics.

License: BSD
"""

import os
import unittest

import data_util


class DataUtilTests(unittest.TestCase):

    def test_query(self):
        query = data_util.Query(
            'test category',
            'test pre category',
            None,
            'test tag',
            None
        )
        self.assertTrue(query.get_has_filters())
        self.assertEqual(
            query.get_id_str(),
            'test category\ttest pre category\tNone\ttest tag\tNone'
        )

    def test_article_set(self):
        category = data_util.Category('a')
        tag = data_util.Tag('b', category)
        keyword = data_util.Keyword('c', category, tag)
        article_set = data_util.ArticleSet(
            'us',
            [category],
            [tag],
            [keyword],
            1
        )
        self.assertTrue(article_set.has_category('a'))
        self.assertFalse(article_set.has_category('b'))

    def test_compressed_data_accessor(self):
        path = os.path.join('txt', 'serialized.txt')
        with open(path) as f:
            lines = f.read().split('\n')
        accessor = data_util.CompressedDataAccessor(lines)

        query = data_util.Query(None, None, None, None, 'security')
        result = accessor.execute_query(query)
        self.assertTrue(result.get_group_count() > 0)
