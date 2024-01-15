import math

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

        query = self._state.get_query()
        self._results = self._accessor.execute_query(query)

        centerpoints_raw = sketch.get_data_layer().get_csv('centerpoints.csv')
        geopoints_flat = map(
            lambda x: (
                x['name'],
                self._sketch.convert_geo_to_pixel(float(x['longitude']), float(x['latitude']))
            ),
            centerpoints_raw
        )
        self._geopoints_dict = dict(geopoints_flat)

        self._sketch.pop_map()

        self._prepare_basemap()

    def check_state(self, mouse_x: float, mouse_y: float):
        countries = self._results.get_countries()
        country_names = map(lambda x: x.get_name(), countries)

        def get_dist(name: str) -> float:
            point = self._geopoints_dict[name]
            dist_x = mouse_x - point[0]
            dist_y = mouse_y - point[1]
            dist = math.sqrt(dist_x**2 + dist_y**2)
            return dist

        countries_with_dist = map(lambda x: (x, get_dist(x)), country_names)
        countries_sorted = sorted(countries_with_dist, key=lambda x: x[1])
        closest_name, closest_dist = countries_sorted[0]

        if closest_dist <= 20:
            self._state.set_country_hovering(closest_name)

    def _prepare_basemap(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.create_buffer('basemap', const.WIDTH, const.HEIGHT)
        self._sketch.enter_buffer('basemap')

        self._sketch.clear_fill()
        self._sketch.set_stroke(const.DEEP_BG_COLOR)
        self._sketch.set_stroke_weight(2)

        for shape in self._geo_shapes:
            self._sketch.draw_shape(shape)

        self._sketch.exit_buffer()

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def draw(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.draw_buffer('basemap', 0, 0)

        self._sketch.set_ellipse_mode('radius')

        country_totals = self._results.get_country_totals()
        country_totals_indexed = dict(map(lambda x: (x.get_name(), x.get_count()), country_totals))

        countries = self._results.get_countries()
        countries_indexed = dict(map(lambda x: (x.get_name(), x), countries))

        for name, loc in self._geopoints_dict.items():
            if name in countries_indexed:
                selected = self._state.get_country_selected() == name
                hovering = self._state.get_country_hovering() == name

                color = const.INACTIVE_COLOR_MAP
                if selected:
                    color = const.ACTIVE_COLOR_MAP
                elif hovering:
                    color = const.HOVER_COLOR_MAP

                if hovering:
                    self._sketch.set_stroke(const.HOVER_COLOR)
                    self._sketch.set_stroke_weight(1)
                else:
                    self._sketch.clear_stroke()

                self._sketch.set_fill(color)

                count = countries_indexed[name].get_count()
                total = country_totals_indexed[name]
                percent = (count + 0.0) / total * 100
                radius = math.sqrt(400.0 / 100 * percent)
                if radius < 1:
                    radius = 1

                self._sketch.draw_ellipse(loc[0], loc[1], radius, radius)

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def refresh_data(self):
        query = self._state.get_query()
        self._results = self._accessor.execute_query(query)
