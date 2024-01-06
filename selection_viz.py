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
        self._placements = []

        query = self._state.get_query()
        self._results = self._accessor.execute_query(query)
        query_active = query.get_has_filters()

        self._tables = []
        for i in range(0, 5):
            self._tables.append(table_util.BarTable(
                self._sketch,
                self._get_prefix(),
                'Top %d %s' % ((i + 1) * 30, self._get_label()),
                self._get_sub_text(query_active)
            ))
            self._placements.append({})

    def check_hover(self, mouse_x: float, mouse_y: float):
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
        for i in range(0, 5):
            target_slice = self._get_results(self._results)[(i*30):((i+1)*30)]
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
        return '% of query' if query_active else '% of all'

    def _get_label(self) -> str:
        raise RuntimeError('Use implementor.')

    def _get_results_raw(self, results: data_util.Result) -> typing.List:
        raise RuntimeError('Use implementor.')
    
    def _get_selected(self, state: state_util.VizState) -> typing.Optional[str]:
        result = self._get_selected_inner(state)
        if result is None:
            return 'All'
        else:
            return result
    
    def _get_hovering(self, state: state_util.VizState) -> typing.Optional[str]:
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

    def _set_hovering(self, state: state_util.VizState, name: str):
        return state.set_country_hovering(name)

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
