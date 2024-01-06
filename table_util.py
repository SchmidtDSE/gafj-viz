import functools
import typing

import sketchingpy

import abstract
import const
import data_util
import state_util


class BarTable:

    def __init__(self, sketch: sketchingpy.Sketch2D, prefix: str, label: str, sub_title: str):
        self._sketch = sketch
        self._prefix = prefix
        self._label = label
        self._sub_title = sub_title

    def set_sub_title(self, sub_title: str):
        self._sub_title = sub_title

    def draw(self, x: int, y: int, groups: data_util.COUNTED_GROUPS,
        selected_name: typing.Optional[str], hovering_name: typing.Optional[str], total_getter,
        prior_placements: typing.Optional[typing.Dict[str, float]] = None,
        placements: typing.Optional[typing.Dict[str, float]] = None,
        count: int = 10, name_overrides: typing.Optional[typing.Dict[str, str]] = None) -> float:

        if name_overrides is None:
            name_overrides = {}

        prefix = self._prefix
        label = self._label
        sub_title = self._sub_title
        
        if prior_placements is None:
            prior_placements = {}
        
        if placements is None:
            placements = {}

        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.set_stroke_weight(1)

        self._sketch.translate(x, 0)

        y += 14
        self._sketch.clear_fill()
        self._sketch.set_stroke(const.INACTIVE_COLOR)
        self._sketch.draw_line(0, y, const.COLUMN_WIDTH, y)

        self._sketch.clear_stroke()
        self._sketch.set_fill(const.INACTIVE_COLOR)
        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 14)
        self._sketch.set_text_align('left', 'baseline')
        self._sketch.draw_text(0, y - 5, label)

        groups_interpreted = self._interpret_groups(groups, total_getter, count)

        for group in groups_interpreted:
            percent = group['percent']
            name = group['name']
            prefix_name = prefix + '_' + name

            color = const.get_color(selected_name == name, hovering_name == name)

            self._sketch.clear_stroke()

            self._sketch.set_rect_mode('center')
            self._sketch.set_fill(const.INACTIVE_COLOR)
            for x in range(0, const.COLUMN_WIDTH + 1, 5):
                self._sketch.draw_rect(x, y + 15, 1, 1)

            self._sketch.set_rect_mode('corner')
            self._sketch.set_fill(color)
            self._sketch.draw_rect(0, y + 15, percent / 100 * const.COLUMN_WIDTH, 2)

            self._sketch.set_fill(color)
            self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 11)
            self._sketch.set_text_align('left', 'baseline')
            self._sketch.draw_text(0, y + 12, name_overrides.get(name, name))

            placements[prefix_name] = y + 6

            self._sketch.set_rect_mode('corner')
            self._sketch.set_fill(const.BG_COLOR_LAYER)
            self._sketch.draw_rect(const.COLUMN_WIDTH - 40, y + 3, 40, 10)

            self._sketch.set_text_align('right', 'baseline')
            self._sketch.set_fill(color)
            self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 10)
            self._sketch.draw_text(const.COLUMN_WIDTH, y + 11, '%.1f%%' % percent)

            if prefix_name in prior_placements:
                self._sketch.clear_fill()
                self._sketch.set_stroke(color + '70')
                self._sketch.set_stroke_weight(1)
                self._sketch.draw_line(
                    -3,
                    placements[prefix_name],
                    -1 * const.COLUMN_PADDING + 3,
                    prior_placements[prefix_name]
                )

            y += 18

        y += 4

        self._sketch.clear_fill()
        self._sketch.set_stroke(const.INACTIVE_COLOR)
        self._sketch.set_stroke_weight(1)
        self._sketch.draw_line(0, y, const.COLUMN_WIDTH, y)

        self._sketch.clear_stroke()
        self._sketch.set_fill(const.INACTIVE_COLOR)
        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 11)
        self._sketch.set_text_align('left', 'top')
        self._sketch.draw_text(0, y + 4, sub_title)

        self._sketch.pop_style()
        self._sketch.pop_transform()

        if len(groups) < count:
            num_missing = count - len(groups)
            y += 18 * num_missing

        return y + 30

    def draw_axis(self, y: int) -> float:
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.translate(0, y)

        self._sketch.clear_fill()
        self._sketch.set_stroke(const.INACTIVE_COLOR)
        self._sketch.draw_line(0, 0, const.COLUMN_WIDTH, 0)

        self._sketch.clear_stroke()
        self._sketch.set_fill(const.INACTIVE_COLOR)
        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 10)
        
        self._sketch.set_text_align('left', 'top')
        self._sketch.draw_text(0, 3, '0%')

        self._sketch.set_text_align('right', 'top')
        self._sketch.draw_text(const.COLUMN_WIDTH, 3, '100%')

        self._sketch.pop_style()
        self._sketch.pop_transform()

        return y + 15

    def _interpret_groups(self, groups: data_util.COUNTED_GROUPS, total_getter,
        count: int) -> typing.Dict:
        def interpret_group(group: data_util.CountedGroup) -> typing.Dict:
            name = group.get_name()
            percent = group.get_count() / (total_getter(group.get_name()) + 0.0) * 100
            return {
                'name': name,
                'percent': percent
            }

        def custom_compare(a, b):
            if a['percent'] == b['percent']:
                if a['name'] < b['name']:
                    return -1
                elif a['name'] > b['name']:
                    return 1
                else:
                    return 0
            else:
                return b['percent'] - a['percent']

        results = [interpret_group(x) for x in groups]
        results.sort(key=functools.cmp_to_key(custom_compare))
        return results[:count]
