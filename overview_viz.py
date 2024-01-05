import abstract

import sketchingpy

import data_util
import state_util


class OverviewViz(abstract.VizMovement):

    def __init__(self, sketch: sketchingpy.Sketch2D, accessor: data_util.DataAccessor,
        state: state_util.VizState):
        self._sketch = sketch
        self._accessor = accessor
        self._state = state

    def check_hover(self, mouse_x: float, mouse_y: float):
        pass

    def draw(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def refresh_data(self):
        pass
