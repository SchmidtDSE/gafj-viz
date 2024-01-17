import unittest

import const


class ConstTests(unittest.TestCase):

    def test_rewrite_noop(self):
        self.assertEqual(const.rewrite('test'), 'test')

    def test_rewrite_action(self):
        self.assertEqual(const.rewrite('people and society'), 'people & society')

    def test_get_color(self):
        self.assertEqual(const.get_color(True, False), const.ACTIVE_COLOR)
        self.assertEqual(const.get_color(False, True), const.HOVER_COLOR)
        self.assertEqual(const.get_color(False, False), const.INACTIVE_COLOR)
