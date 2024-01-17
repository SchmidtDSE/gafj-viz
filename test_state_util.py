import unittest

import state_util


class StateUtilTest(unittest.TestCase):

    def test_toggle(self):
        state = state_util.VizState()
        self.assertIsNone(state.get_category_selected())

        state.toggle_category_selected('test')
        self.assertEqual(state.get_category_selected(), 'test')

        state.toggle_category_selected('test')
        self.assertIsNone(state.get_category_selected())

    def test_get_query(self):
        state = state_util.VizState()
        query = state.get_query()
        self.assertIsNone(query.get_keyword())

        state.toggle_keyword_selected('test')
        query = state.get_query()
        self.assertEqual(query.get_keyword(), 'test')

    def test_serialize_equal(self):
        state_1 = state_util.VizState()
        state_2 = state_util.VizState()
        self.assertEqual(state_1.serialize(), state_2.serialize())

        state_1.toggle_category_selected('test')
        self.assertNotEqual(state_1.serialize(), state_2.serialize())

        state_2.toggle_category_selected('test')
        self.assertEqual(state_1.serialize(), state_2.serialize())
