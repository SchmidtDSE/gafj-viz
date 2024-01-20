import math
import typing

import sketchingpy

import abstract
import const
import data_util
import state_util
import table_util


class SelectionMovement(abstract.VizMovement):

    def __init__(self, sketch: sketchingpy.Sketch2D, accessor: data_util.DataAccessor,
        state: state_util.VizState):
        self._sketch = sketch
        self._accessor = accessor
        self._state = state
        self._placements: typing.List[typing.Dict[str, int]] = []

        query = self._state.get_query()
        self._results = self._accessor.execute_query(query)
        query_active = query.get_has_filters()

        self._tables = []
        for i in range(0, 5):
            self._tables.append(table_util.BarTable(
                self._sketch,
                self._get_prefix(),
                'Top %d %s' % ((i + 1) * 30, self._get_label()),
                self._get_sub_text(query_active),
                False
            ))
            self._placements.append({})

    def check_state(self, mouse_x: float, mouse_y: float):
        group_number = math.floor(mouse_x / (const.COLUMN_WIDTH + 10) - 5)
        if group_number >= len(self._tables):
            return

        placements = self._placements[group_number]

        self._set_hovering(self._state, None)
        for prefix_name, y in placements.items():
            if abs(y - mouse_y) < 10:
                prefix, name = prefix_name.split('_')
                self._set_hovering(self._state, name)

    def draw(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        for i in range(0, 5):
            start_i = i * 30
            end_i = (i + 1) * 30
            target_slice = self._get_results(self._results)[start_i:end_i]
            placements = self._placements[i]
            placements.clear()
            if len(target_slice) > 0:
                self._tables[i].draw(
                    5 + i * (const.COLUMN_WIDTH + 10),
                    90,
                    target_slice,
                    self._get_selected(self._state),
                    self._get_hovering(self._state),
                    lambda x: self._get_total(self._results, x),
                    {},
                    placements,
                    count=30,
                    name_overrides={'All': 'All ' + self._get_label()}
                )

        self._sketch.set_rect_mode('corner')
        self._sketch.clear_stroke()
        self._sketch.set_fill(const.DEEP_BG_COLOR)
        self._sketch.draw_rect(0, 0, const.WIDTH, 50)

        self._sketch.set_text_font(const.FONT, 30)
        self._sketch.set_text_align('left', 'center')
        self._sketch.set_fill(const.INACTIVE_COLOR)
        self._sketch.draw_text(5, 25, 'Selecting from ' + self._get_label())

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def refresh_data(self):
        query = self._state.get_query()
        self._results = self._accessor.execute_query(query)

        query_active = self._results.get_has_filters()
        sub_title = self._get_sub_text(query_active)
        for table in self._tables:
            table.set_sub_title(sub_title)

    def _get_results(self, results: data_util.Result):
        return [data_util.CountedGroup('All', 1)] + self._get_results_raw(results)

    def _get_prefix(self) -> str:
        return 'default'

    def _get_sub_text(self, query_active: bool) -> str:
        return '% of query' if query_active else '% of all articles'

    def _get_label(self) -> str:
        raise RuntimeError('Use implementor.')

    def _get_results_raw(self, results: data_util.Result) -> typing.List:
        raise RuntimeError('Use implementor.')

    def _get_selected(self, state: state_util.VizState) -> typing.Optional[str]:
        return self._get_selected_inner(state)

    def _get_selected_inner(self, state: state_util.VizState) -> typing.Optional[str]:
        raise RuntimeError('Use implementor.')

    def _get_hovering(self, state: state_util.VizState) -> typing.Optional[str]:
        raise RuntimeError('Use implementor.')

    def _set_hovering(self, state: state_util.VizState, name: typing.Optional[str]):
        raise RuntimeError('Use implementor.')

    def _get_total(self, results: data_util.Result, name: str) -> int:
        if name == 'All':
            return 1
        else:
            return self._get_total_inner(results, name)

    def _get_total_inner(self, results: data_util.Result, name: str) -> int:
        raise RuntimeError('Use implementor.')


class CountrySelectionMovement(SelectionMovement):

    def _get_label(self) -> str:
        return 'Countries'

    def _get_results_raw(self, results: data_util.Result):
        return results.get_countries()

    def _get_selected_inner(self, state: state_util.VizState):
        return state.get_country_selected()

    def _get_hovering(self, state: state_util.VizState):
        return state.get_country_hovering()

    def _set_hovering(self, state: state_util.VizState, name: typing.Optional[str]):
        if name:
            state.set_country_hovering(name)
        else:
            state.clear_country_hovering()

    def _get_total_inner(self, results: data_util.Result, name: str) -> int:
        country_totals = results.get_country_totals()
        matching = filter(lambda x: x.get_name() == name, country_totals)
        matching_first = next(matching, None)
        if matching_first is None:
            return 0
        else:
            return matching_first.get_count()

    def _get_sub_text(self, query_active: bool) -> str:
        return '% of all in country'


class CategorySelectionMovement(SelectionMovement):

    def _get_label(self) -> str:
        return 'Categories'

    def _get_results_raw(self, results: data_util.Result):
        return results.get_categories()

    def _get_selected_inner(self, state: state_util.VizState):
        return state.get_category_selected()

    def _get_hovering(self, state: state_util.VizState):
        return state.get_category_hovering()

    def _set_hovering(self, state: state_util.VizState, name: typing.Optional[str]):
        if name:
            state.set_category_hovering(name)
        else:
            state.clear_category_hovering()

    def _get_total_inner(self, results: data_util.Result, name: str) -> int:
        return results.get_total_count()

    def _get_sub_text(self, query_active: bool) -> str:
        return '% of query' if query_active else '% of all articles'


class TagSelectionMovement(SelectionMovement):

    def _get_label(self) -> str:
        return 'Tags'

    def _get_results_raw(self, results: data_util.Result):
        return results.get_tags()

    def _get_selected_inner(self, state: state_util.VizState):
        return state.get_tag_selected()

    def _get_hovering(self, state: state_util.VizState):
        return state.get_tag_hovering()

    def _set_hovering(self, state: state_util.VizState, name: typing.Optional[str]):
        if name:
            state.set_tag_hovering(name)
        else:
            state.clear_tag_hovering()

    def _get_total_inner(self, results: data_util.Result, name: str) -> int:
        return results.get_total_count()

    def _get_sub_text(self, query_active: bool) -> str:
        return '% of query' if query_active else '% of all articles'


class KeywordSelectionMovement(SelectionMovement):

    def _get_label(self) -> str:
        return 'Keywords'

    def _get_results_raw(self, results: data_util.Result):
        return results.get_keywords()

    def _get_selected_inner(self, state: state_util.VizState):
        return state.get_keyword_selected()

    def _get_hovering(self, state: state_util.VizState):
        return state.get_keyword_hovering()

    def _set_hovering(self, state: state_util.VizState, name: typing.Optional[str]):
        if name:
            state.set_keyword_hovering(name)
        else:
            state.clear_keyword_hovering()

    def _get_total_inner(self, results: data_util.Result, name: str) -> int:
        return results.get_total_count()

    def _get_sub_text(self, query_active: bool) -> str:
        return '% of query' if query_active else '% of all articles'
