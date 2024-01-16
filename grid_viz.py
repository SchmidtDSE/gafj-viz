import typing

import sketchingpy

import abstract
import const
import data_util
import state_util
import table_util


class GridColumn:

    def __init__(self, sketch: sketchingpy.Sketch2D, category: str, x: int,
        results: data_util.Result):
        self._sketch = sketch
        self._category = category
        self._x = x
        self._placements: typing.Dict[str, float] = {}
        self._results = results

        query_active = results.get_has_filters()
        self._header_description = 'of query' if query_active else 'of all'

        self._tags_table = table_util.BarTable(
            self._sketch,
            'tags',
            'Top Tags',
            '% of category in query' if query_active else '% of category',
            True
        )
        self._keywords_table = table_util.BarTable(
            self._sketch,
            'keywords',
            'Top Keywords',
            '% of category in query' if query_active else '% of category',
            True
        )
        self._countries_table = table_util.BarTable(
            self._sketch,
            'countries',
            'Top Countries',
            '% of all in country',
            True
        )

    def get_category(self) -> str:
        return self._category

    def set_results(self, results: data_util.Result):
        query_active = results.get_has_filters()
        sub_title = '% of category in query' if query_active else '% of category'
        self._tags_table.set_sub_title(sub_title)
        self._keywords_table.set_sub_title(sub_title)
        self._header_description = 'of query' if query_active else 'of all'

        self._results = results

    def check_state(self, current_state: state_util.VizState, mouse_x: float, mouse_y: float):
        if mouse_x < self._x or mouse_x > self._x + const.COLUMN_WIDTH:
            return

        if abs(80 - mouse_y) < 50:
            current_state.set_category_hovering(self._category)

        for prefix_name, y in self._placements.items():
            if abs(y - mouse_y) < 10:
                prefix, name = prefix_name.split('_')

                if prefix == 'tags':
                    current_state.set_tag_hovering(name)
                elif prefix == 'keywords':
                    current_state.set_keyword_hovering(name)
                elif prefix == 'countries':
                    current_state.set_country_hovering(name)

                return

    def get_placements(self) -> typing.Dict[str, float]:
        return self._placements

    def draw(self, current_state: state_util.VizState, prior_placements: typing.Dict[str, float]):
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.translate(self._x, 0)

        y = 0.0

        category_selected = current_state.get_category_selected() == self._category
        category_hovering = current_state.get_category_hovering() == self._category
        y = self._draw_header(y, category_selected, category_hovering)

        self._placements.clear()

        y = self._tags_table.draw(
            0,
            y,
            self._results.get_tags(),
            current_state.get_tag_selected(),
            current_state.get_tag_hovering(),
            lambda x: self._results.get_total_count(),
            prior_placements=prior_placements,
            placements=self._placements,
            count=7
        )

        y = self._keywords_table.draw(
            0,
            y,
            self._results.get_keywords(),
            current_state.get_keyword_selected(),
            current_state.get_keyword_hovering(),
            lambda x: self._results.get_total_count(),
            prior_placements=prior_placements,
            placements=self._placements,
            count=7
        )

        country_totals = self._results.get_country_totals()
        country_totals_indexed = dict(map(lambda x: (x.get_name(), x.get_count()), country_totals))

        y = self._countries_table.draw(
            0,
            y,
            self._results.get_countries(),
            current_state.get_country_selected(),
            current_state.get_country_hovering(),
            lambda x: country_totals_indexed[x],
            prior_placements,
            self._placements,
            count=7
        )

        y = self._countries_table.draw_axis(0, y)

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def _draw_header(self, y: float, selected: bool, hovering: bool):
        self._sketch.push_transform()
        self._sketch.push_style()

        color = const.get_color(selected, hovering)

        self._sketch.translate(const.COLUMN_WIDTH / 2, y + 70)

        group_count = self._results.get_group_count()
        total_count = self._results.get_total_count()

        category_percent = 0.0
        if total_count != 0:
            category_percent = (group_count + 0.0) / total_count * 100

        end_angle = category_percent / 100 * 360
        self._sketch.set_arc_mode('radius')
        self._sketch.set_angle_mode('degrees')
        self._sketch.clear_fill()
        self._sketch.set_stroke_weight(10)
        self._sketch.set_stroke(const.DEEP_BG_COLOR)
        self._sketch.draw_arc(0, 0, 50, 50, 0, 360)
        self._sketch.set_stroke(color)
        self._sketch.draw_arc(0, 0, 50, 50, 0, end_angle)

        self._sketch.clear_stroke()
        self._sketch.set_fill(const.DEEP_BG_COLOR)
        self._sketch.set_rect_mode('radius')
        self._sketch.draw_rect(0, -13, 85, 10)

        self._sketch.clear_stroke()
        self._sketch.set_fill(color)
        self._sketch.set_text_font(const.FONT, 14)
        self._sketch.set_text_align('center', 'baseline')
        self._sketch.draw_text(0, -8, const.REWRITES.get(self._category, self._category))

        self._sketch.set_text_font(const.FONT, 11)
        self._sketch.set_text_align('center', 'top')
        self._sketch.draw_text(0, 2, '%.1f%%' % category_percent)
        self._sketch.draw_text(0, 14, self._header_description)

        self._sketch.pop_style()
        self._sketch.pop_transform()

        return 140


class GridViz(abstract.VizMovement):

    def __init__(self, sketch: sketchingpy.Sketch2D, accessor: data_util.DataAccessor,
        state: state_util.VizState):
        self._sketch = sketch
        self._accessor = accessor
        self._state = state

        self._columns = [
            self._build_column('people and society', 0),
            self._build_column('economy and industry', 1),
            self._build_column('food and materials', 2),
            self._build_column('health and body', 3),
            self._build_column('environment and resources', 4)
        ]

    def check_state(self, mouse_x: float, mouse_y: float):
        for column in self._columns:
            column.check_state(self._state, mouse_x, mouse_y)

    def draw(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        placements = {}
        for column in self._columns:
            column.draw(self._state, placements)
            placements = column.get_placements()

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def refresh_data(self):
        for column in self._columns:
            new_results = self._get_results_for_category(column.get_category())
            column.set_results(new_results)

    def _build_column(self, category: str, i: int) -> GridColumn:
        results = self._get_results_for_category(category)
        return GridColumn(
            self._sketch,
            category,
            5 + (const.COLUMN_WIDTH + const.COLUMN_PADDING) * i,
            results
        )

    def _get_results_for_category(self, category: str) -> data_util.Result:
        query = self._state.get_query(category)
        return self._accessor.execute_query(query)
