import sketchingpy

import abstract
import const
import data_util
import state_util


class MapViz(abstract.VizMovement):

    def __init__(self, sketch: sketchingpy.Sketch2D, accessor: data_util.DataAccessor,
        state: state_util.VizState, center_x: float, center_y: float):
        self._sketch = sketch
        self._accessor = accessor
        self._state = state

        self._center_x = center_x
        self._center_y = center_y

        self._sketch.push_map()

        self._sketch.set_map_pan(0, 0)
        self._sketch.set_map_placement(self._center_x, self._center_y)
        self._sketch.set_map_zoom(0.2)

        source = sketch.get_data_layer().get_json('zoomed_out.geojson')
        geo_polygons = sketch.parse_geojson(source)
        self._geo_shapes = [x.to_shape() for x in geo_polygons]

        self._sketch.pop_map()

    def check_hover(self, mouse_x: float, mouse_y: float):
        pass

    def draw(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.clear_fill()
        self._sketch.set_stroke(const.DEEP_BG_COLOR)
        self._sketch.set_stroke_weight(2)

        for shape in self._geo_shapes:
            self._sketch.draw_shape(shape)

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def refresh_data(self):
        pass
