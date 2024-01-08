import abstract

import sketchingpy

import const
import data_util
import map_viz
import state_util
import table_util


class OverviewViz(abstract.VizMovement):

    def __init__(self, sketch: sketchingpy.Sketch2D, accessor: data_util.DataAccessor,
        state: state_util.VizState):
        self._sketch = sketch
        self._accessor = accessor
        self._state = state
        self._placements = {}

        query = self._state.get_query()
        self._results = self._accessor.execute_query(query)

        query_active = self._results.get_has_filters()

        self._categories_table = table_util.BarTable(
            self._sketch,
            'categories',
            'Categories',
            '% of query' if query_active else '% of all',
            True
        )
        self._tags_table = table_util.BarTable(
            self._sketch,
            'tags',
            'Top Tags',
            '% of query' if query_active else '% of all',
            True
        )
        self._keywords_table = table_util.BarTable(
            self._sketch,
            'keywords',
            'Top Keywords',
            '% of query' if query_active else '% of all',
            True
        )
        self._countries_table = table_util.BarTable(
            self._sketch,
            'countries',
            'Countries',
            '% of all in country',
            True
        )

        self._map_component = map_viz.MapViz(
            self._sketch,
            self._accessor,
            self._state,
            const.WIDTH / 5 * 2,
            const.HEIGHT / 4 * 3
        )

    def check_state(self, mouse_x: float, mouse_y: float):
        def check_state_prefix(x: int, prefix: str):
            if mouse_x < x or mouse_x > x + const.COLUMN_WIDTH:
                return

            for prefix_name, y in self._placements.items():
                candidate_prefix, name = prefix_name.split('_')
                if abs(y - mouse_y) < 10 and candidate_prefix == prefix:
                    if prefix == 'tags':
                        self._state.set_tag_hovering(name)
                    elif prefix == 'keywords':
                        self._state.set_keyword_hovering(name)
                    elif prefix == 'countries':
                        self._state.set_country_hovering(name)
                    elif prefix == 'categories':
                        self._state.set_category_hovering(name)

        x = const.WIDTH - const.COLUMN_WIDTH - 30
        check_state_prefix(x, 'countries')
        
        x -= const.COLUMN_WIDTH + 20
        check_state_prefix(x, 'keywords')

        x -= const.COLUMN_WIDTH + 20
        check_state_prefix(x, 'tags')

        x -= const.COLUMN_WIDTH + 20
        check_state_prefix(x, 'categories')

        self._map_component.check_state(mouse_x, mouse_y)

    def draw(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        x = const.WIDTH - const.COLUMN_WIDTH - 30

        country_totals = self._results.get_country_totals()
        country_totals_indexed = dict(map(lambda x: (x.get_name(), x.get_count()), country_totals))

        self._placements.clear()

        countries_y_end = self._countries_table.draw(
            x,
            10,
            self._results.get_countries(),
            self._state.get_country_selected(),
            self._state.get_country_hovering(),
            lambda x: country_totals_indexed[x],
            {},
            self._placements,
            count=30
        )

        self._countries_table.draw_axis(x, countries_y_end, include_circles=True)

        x -= const.COLUMN_WIDTH + 20
        self._keywords_table.draw(
            x,
            10,
            self._results.get_keywords(),
            self._state.get_keyword_selected(),
            self._state.get_keyword_hovering(),
            lambda x: self._results.get_total_count(),
            {},
            self._placements
        )

        x -= const.COLUMN_WIDTH + 20
        self._tags_table.draw(
            x,
            10,
            self._results.get_tags(),
            self._state.get_tag_selected(),
            self._state.get_tag_hovering(),
            lambda x: self._results.get_total_count(),
            {},
            self._placements
        )

        x -= const.COLUMN_WIDTH + 20
        self._categories_table.draw(
            x,
            10,
            self._results.get_categories(),
            self._state.get_category_selected(),
            self._state.get_category_hovering(),
            lambda x: self._results.get_total_count(),
            {},
            self._placements
        )

        self._map_component.draw()

        self._sketch.clear_stroke()
        self._sketch.set_fill(const.INACTIVE_COLOR)
        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 11)
        self._sketch.set_text_align('left', 'center')
        self._sketch.draw_text(
            const.WIDTH - const.COLUMN_WIDTH - 30,
            countries_y_end + 100,
            'Click to add filter. Click again\nto remove filter.'
        )

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def refresh_data(self):
        query = self._state.get_query()
        self._results = self._accessor.execute_query(query)

        query_active = self._results.get_has_filters()
        sub_title = '% of query' if query_active else '% of all'
        self._categories_table.set_sub_title(sub_title)
        self._tags_table.set_sub_title(sub_title)
        self._keywords_table.set_sub_title(sub_title)

        self._map_component.refresh_data()
