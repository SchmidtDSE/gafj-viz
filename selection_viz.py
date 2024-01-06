import abstract

import sketchingpy

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
        self._placements = {}

        query = self._state.get_query()
        self._results = self._accessor.execute_query(query)

        self._tables = []
        for i in range(0, 5):
            self._tables.append(table_util.BarTable(
                self._sketch,
                self._get_prefix(),
                'Top %d %s' % ((i + 1) * 30, self._get_label()),
                '% of query' if query_active else '% of all'
            ))

    def check_hover(self, mouse_x: float, mouse_y: float):
        raise RuntimeError('Use implementor.')

    def draw(self):
        self._placements.clear()

        for i in range(0, 5):
            target_slice = self._get_results(self._results)[(i*30):((i+1)*30)]
            if len(target_slice) > 0:
                self._tables[i].draw(
                    5 + i * (const.COLUMN_WIDTH + 10),
                    70,
                    target_slice,
                    self._get_selected(self._state),
                    self._get_hovering(self._state),
                    lambda x: self._results.get_total_count(),
                    {},
                    self._placements,
                    count=30
                )

    def refresh_data(self):
        query = self._state.get_query()
        self._results = self._accessor.execute_query(query)

        query_active = self._results.get_has_filters()
        sub_title = '% of query' if query_active else '% of all'
        for table in self._tables:
            table.set_sub_title(sub_title)

    def _get_results(self, results: data_util.Result):
        return self._get_results_raw(results)

    def _get_results_raw(self, results: data_util.Result):
        raise RuntimeError('Use implementor.')
    
    def _get_selected(self, state: state_util.VizState):
        raise RuntimeError('Use implementor.')
    
    def _get_hovering(self, state: state_util.VizState):
        raise RuntimeError('Use implementor.')
