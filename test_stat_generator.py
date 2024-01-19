import article_getter
import article_stat_gen

import unittest


class TestStatGenerator(unittest.TestCase):

    def test_stat_generator(self):
        inner_getter = article_getter.LocalArticleGetter()
        generator = article_stat_gen.StatGenerator(inner_getter)
        result = generator.execute({
            'keyword': 'security',
            'dimension': 'keyword'
        })
        self.assertAlmostEqual(result['security'], 1)

    def test_country_percent(self):
        inner_getter = article_getter.LocalArticleGetter()
        generator = article_stat_gen.StatGenerator(inner_getter)
        result = generator.execute({
            'keyword': 'security',
            'dimension': 'country'
        })
        self.assertTrue(result['Australia'] > 0)
