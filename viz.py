import typing

import sketching

import data_util
import state_util

BG_COLOR = '#505050'
BG_COLOR_LAYER = '#505050A0'
DEEP_BG_COLOR = '#303030C0'

COLUMN_WIDTH = 200
COLUMN_PADDING = 50

INACTIVE_COLOR = '#D0D0D0'
ACTIVE_COLOR = '#A6CEE3'
HOVER_COLOR = '#B2DF8A'

REWRITES = {
    'people and society': 'people & society',
    'economy and industry': 'econ & industry',
    'food and materials': 'food & materials',
    'health and body': 'health & body',
    'environment and resources': 'env & resource'
}


class VizColumn:

    def __init__(self, sketch: sketching.Sketch2D, category: str, x: int,
        results: data_util.Result):
        self._sketch = sketch
        self._category = category
        self._x = x
        self._placements: typing.Dict[str, float] = {}
        self._results = results

    def set_results(self, results: data_util.Result):
        self._results = results

    def check_hover(self, current_state: state_util.VizState, mouse_x: float, mouse_y: float):
        if mouse_x < self._x or mouse_x > self._x + COLUMN_WIDTH:
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

        y = 0

        category_selected = current_state.get_category_selected() == self._category
        category_hovering = current_state.get_category_hovering() == self._category
        y = self._draw_header(y, category_selected, category_hovering)

        y = self._draw_counted_groups(
            'tags',
            'Top Tags',
            '% of category',
            y,
            self._results.get_tags(),
            current_state.get_tag_selected(),
            current_state.get_tag_hovering(),
            lambda x: self._results.get_group_count(),
            prior_placements,
            self._placements
        )
        
        y = self._draw_counted_groups(
            'keywords',
            'Top Keywords',
            '% of category',
            y,
            self._results.get_keywords(),
            current_state.get_keyword_selected(),
            current_state.get_keyword_hovering(),
            lambda x: self._results.get_group_count(),
            prior_placements,
            self._placements
        )
        
        country_totals = self._results.get_country_totals()
        country_totals_indexed = dict(map(lambda x: (x.get_name(), x.get_count()), country_totals))

        y = self._draw_counted_groups(
            'countries',
            'Countries',
            '% of country',
            y,
            self._results.get_countries(),
            current_state.get_country_selected(),
            current_state.get_country_hovering(),
            lambda x: country_totals_indexed[x],
            prior_placements,
            self._placements
        )

        y = self._draw_axis(y)

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def _draw_axis(self, y: int):
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.translate(0, y)

        self._sketch.clear_fill()
        self._sketch.set_stroke(INACTIVE_COLOR)
        self._sketch.draw_line(0, 0, COLUMN_WIDTH, 0)

        self._sketch.clear_stroke()
        self._sketch.set_fill(INACTIVE_COLOR)
        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 10)
        
        self._sketch.set_text_align('left', 'top')
        self._sketch.draw_text(0, 3, '0%')

        self._sketch.set_text_align('right', 'top')
        self._sketch.draw_text(COLUMN_WIDTH, 3, '100%')

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def _draw_header(self, y: int, selected: bool, hovering: bool):
        self._sketch.push_transform()
        self._sketch.push_style()

        color = self._get_color(selected, hovering)

        self._sketch.translate(COLUMN_WIDTH / 2, y + 80)

        group_count = self._results.get_group_count()
        total_count = self._results.get_total_count()
        category_percent = (group_count + 0.0) / total_count * 100
        end_angle = category_percent / 100 * 360
        self._sketch.set_arc_mode('radius')
        self._sketch.set_angle_mode('degrees')
        self._sketch.clear_fill()
        self._sketch.set_stroke_weight(10)
        self._sketch.set_stroke(DEEP_BG_COLOR)
        self._sketch.draw_arc(0, 0, 50, 50, 0, 360)
        self._sketch.set_stroke(color)
        self._sketch.draw_arc(0, 0, 50, 50, 0, end_angle)

        self._sketch.clear_stroke()
        self._sketch.set_fill(DEEP_BG_COLOR)
        self._sketch.set_rect_mode('radius')
        self._sketch.draw_rect(0, -10, 85, 10)

        self._sketch.clear_stroke()
        self._sketch.set_fill(color)
        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 14)
        self._sketch.set_text_align('center', 'baseline')
        self._sketch.draw_text(0, -5, REWRITES.get(self._category, self._category))

        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 11)
        self._sketch.set_text_align('center', 'top')
        self._sketch.draw_text(0, 5, '%.1f%%' % category_percent)

        self._sketch.pop_style()
        self._sketch.pop_transform()

        return 160

    def _interpret_groups(self, groups: data_util.COUNTED_GROUPS, total_getter,
        count: int) -> typing.Dict:
        def interpret_group(group: data_util.CountedGroup) -> typing.Dict:
            name = group.get_name()
            percent = group.get_count() / (total_getter(group.get_name()) + 0.0) * 100
            return {
                'name': name,
                'percent': percent
            }

        results = [interpret_group(x) for x in groups]
        results.sort(key=lambda x: x['percent'], reverse=True)
        return results[:count]

    def _draw_counted_groups(self, prefix: str, label: str, sub_title: str, y: int,
        groups: data_util.COUNTED_GROUPS, selected_name: typing.Optional[str],
        hovering_name: typing.Optional[str], total_getter,
        prior_placements: typing.Dict[str, float], placements: typing.Dict[str, float],
        count: int = 10):
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.set_stroke_weight(2)

        y += 14
        self._sketch.clear_fill()
        self._sketch.set_stroke(INACTIVE_COLOR)
        self._sketch.draw_line(0, y, COLUMN_WIDTH, y)

        self._sketch.clear_stroke()
        self._sketch.set_fill(INACTIVE_COLOR)
        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 14)
        self._sketch.set_text_align('left', 'baseline')
        self._sketch.draw_text(0, y - 5, label)

        groups_interpreted = self._interpret_groups(groups, total_getter, count)

        for group in groups_interpreted:
            percent = group['percent']
            name = group['name']
            prefix_name = prefix + '_' + name

            color = self._get_color(selected_name == name, hovering_name == name)

            self._sketch.clear_stroke()

            self._sketch.set_rect_mode('center')
            self._sketch.set_fill(INACTIVE_COLOR)
            for x in range(0, COLUMN_WIDTH + 1, 5):
                self._sketch.draw_rect(x, y + 15, 1, 1)

            self._sketch.set_rect_mode('corner')
            self._sketch.set_fill(color)
            self._sketch.draw_rect(0, y + 15, percent / 100 * COLUMN_WIDTH, 2)

            self._sketch.set_fill(color)
            self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 11)
            self._sketch.set_text_align('left', 'baseline')
            self._sketch.draw_text(0, y + 12, name)

            placements[prefix_name] = y + 6

            self._sketch.set_rect_mode('corner')
            self._sketch.set_fill(BG_COLOR_LAYER)
            self._sketch.draw_rect(COLUMN_WIDTH - 40, y + 3, 40, 10)

            self._sketch.set_text_align('right', 'baseline')
            self._sketch.set_fill(color)
            self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 10)
            self._sketch.draw_text(COLUMN_WIDTH, y + 11, '%.1f%%' % percent)

            if prefix_name in prior_placements:
                self._sketch.clear_fill()
                self._sketch.set_stroke(color + '70')
                self._sketch.set_stroke_weight(1)
                self._sketch.draw_line(
                    -3,
                    placements[prefix_name],
                    -1 * COLUMN_PADDING + 3,
                    prior_placements[prefix_name]
                )

            y += 18

        y += 4

        self._sketch.clear_fill()
        self._sketch.set_stroke(INACTIVE_COLOR)
        self._sketch.draw_line(0, y, COLUMN_WIDTH, y)

        self._sketch.clear_stroke()
        self._sketch.set_fill(INACTIVE_COLOR)
        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 11)
        self._sketch.set_text_align('left', 'top')
        self._sketch.draw_text(0, y + 4, sub_title)

        self._sketch.pop_style()
        self._sketch.pop_transform()

        if len(groups) < count:
            num_missing = count - len(groups)
            y += 18 * num_missing

        return y + 30

    def _get_color(self, selected: bool, hovering: bool) -> str:
        if selected:
            return ACTIVE_COLOR
        elif hovering:
            return HOVER_COLOR
        else:
            return INACTIVE_COLOR


class NewsVisualization:

    def __init__(self):
        self._changed = True
        self._drawn = False
        self._state = state_util.VizState()
        self._accessor = data_util.LocalDataAccessor()
        self._sketch = sketching.Sketch2D(1225, 900, 'News Visualization')
        self._sketch.set_fps(20)

        self._columns = [
            self._build_column('people and society', 0),
            self._build_column('economy and industry', 1),
            self._build_column('food and materials', 2),
            self._build_column('health and body', 3),
            self._build_column('environment and resources', 4)
        ]

        self._sketch.on_step(lambda x: self._draw())

    def show(self):
        self._sketch.show()

    def _draw(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        if self._drawn:
            prior_state_str = self._state.serialize()
            
            self._state.clear_category_hovering()
            self._state.clear_country_hovering()
            self._state.clear_keyword_hovering()
            self._state.clear_tag_hovering()

            mouse = self._sketch.get_mouse()
            mouse_x = mouse.get_pointer_x()
            mouse_y = mouse.get_pointer_y()
            for column in self._columns:
                column.check_hover(self._state, mouse_x, mouse_y)
            self._changed = prior_state_str != self._state.serialize()

        if self._changed:
            self._sketch.clear(BG_COLOR)

            placements = {}
            for column in self._columns:
                column.draw(self._state, placements)
                placements = column.get_placements()

            self._drawn = True
            self._changed = False

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def _build_column(self, category: str, i: int) -> VizColumn:
        results = self._get_results_for_category(category)
        return VizColumn(self._sketch, category, 5 + (COLUMN_WIDTH + COLUMN_PADDING) * i, results)

    def _get_results_for_category(self, category: str) -> data_util.Result:
        query = self._state.get_query(category)
        return self._accessor.execute_query(query)



def main():
    visualization = NewsVisualization()
    visualization.show()


if __name__ == '__main__':
    main()
