import typing

import sketchingpy

import data_util
import state_util

import const
import grid_viz
import overview_viz
import selection_viz


class NewsVisualization:

    def __init__(self):
        self._changed = True
        self._drawn = False
        self._state = state_util.VizState()
        self._sketch = sketchingpy.Sketch2D(const.WIDTH, const.HEIGHT, 'News Visualization')
        self._sketch.set_fps(15)

        self._movement = 'overview'
        self._button_hover = 'none'
        self._last_major_movement = 'overview'

        data_layer = self._sketch.get_data_layer()
        compressed_data = data_layer.get_text('serialized.txt')
        compressed_lines = compressed_data.split('\n')
        self._accessor = data_util.CompressedDataAccessor(compressed_lines)

        self._overview = overview_viz.OverviewViz(self._sketch, self._accessor, self._state)
        self._grid = grid_viz.GridViz(self._sketch, self._accessor, self._state)
        self._selectors = {
            'country': selection_viz.CountrySelectionMovement(self._sketch, self._accessor, self._state)
        }

        self._sketch.on_step(lambda sketch: self._draw())
        self._sketch.get_mouse().on_button_press(
            lambda button: self._respond_to_click(button)
        )

    def show(self):
        self._sketch.show()

    def _draw(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        target_viz = {
            'overview': self._overview,
            'grid': self._grid,
            'country': self._selectors['country']
        }[self._movement]

        if self._drawn:
            prior_state_str = self._state.serialize()

            self._state.clear_category_hovering()
            self._state.clear_country_hovering()
            self._state.clear_keyword_hovering()
            self._state.clear_tag_hovering()

            mouse = self._sketch.get_mouse()
            mouse_x = mouse.get_pointer_x()
            mouse_y = mouse.get_pointer_y()

            target_viz.check_hover(mouse_x, mouse_y)

            in_footer = mouse_y > const.BUTTON_Y
            button_hover_hold = self._button_hover
            self._button_hover = 'none'
            if in_footer:
                if mouse_x > const.BUTTON_X:
                    self._button_hover = 'button'

                def in_dropdown(x: int) -> bool:
                    return mouse_x > x and mouse_x < (x + 185)

                if in_dropdown(200 + 185 * 0):
                    self._button_hover = 'countries'
                elif in_dropdown(200 + 185 * 1):
                    self._button_hover = 'categories'
                elif in_dropdown(200 + 185 * 2):
                    self._button_hover = 'tags'
                elif in_dropdown(200 + 185 * 3):
                    self._button_hover = 'keywords'

            button_hover_change = button_hover_hold != self._button_hover
            global_ui_change = button_hover_change

            self._changed = prior_state_str != self._state.serialize() or global_ui_change

        if self._changed:
            self._sketch.clear(const.BG_COLOR)

            target_viz.draw()

            self._draw_footer()

            self._drawn = True
            self._changed = False

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def _respond_to_click(self, button):
        if button.get_name() != 'leftMouse':
            return

        category = self._state.get_category_hovering()
        if category is not None:
            self._state.set_category_selected(category)

        country = self._state.get_country_hovering()
        if country is not None:
            self._state.set_country_selected(country)

        keyword = self._state.get_keyword_hovering()
        if keyword is not None:
            self._state.set_keyword_selected(keyword)

        tag = self._state.get_tag_hovering()
        if tag is not None:
            self._state.set_tag_selected(tag)

        if self._button_hover == 'button':
            if self._movement == 'overview':
                self._movement = 'grid'
                self._last_major_movement = 'grid'
            elif self._movement == 'grid':
                self._movement = 'overview'
                self._last_major_movement = 'overview'
            else:
                self._movement = self._last_major_movement
        elif self._button_hover == 'countries':
            self._movement = 'country'

        self._grid.refresh_data()
        self._overview.refresh_data()

        self._changed = True
        self._drawn = False

    def _draw_footer(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        text_y = const.SELECTOR_Y + const.SELECTOR_HEIGHT - 16

        def draw_select(x: int, text: str, state: str):
            hovering = state == self._button_hover

            self._sketch.clear_fill()
            self._sketch.set_stroke(const.HOVER_COLOR if hovering else const.INACTIVE_COLOR)
            self._sketch.draw_rect(x, text_y - 18, 180, 24)

            self._sketch.clear_stroke()
            self._sketch.set_fill(const.HOVER_COLOR if hovering else const.INACTIVE_COLOR)
            self._sketch.draw_text(x + 5, text_y, text)
            self._sketch.draw_text(x + 180 - 12, text_y, '>')

        def make_label(value: typing.Optional[str], default_val: str) -> str:
            label = value if value else default_val
            if len(label) > 15:
                return label[:15] + '...'
            else:
                return label

        # Draw selector
        self._sketch.set_fill(const.DEEP_BG_COLOR)
        self._sketch.set_rect_mode('corner')
        self._sketch.draw_rect(
            const.SELECTOR_X,
            const.SELECTOR_Y,
            const.SELECTOR_WIDTH,
            const.SELECTOR_HEIGHT
        )

        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 14)
        self._sketch.set_text_align('left', 'baseline')
        self._sketch.set_fill(const.INACTIVE_COLOR)

        x = 10
        self._sketch.draw_text(x, text_y, 'Showing articles from')
        
        x += 190
        country_selected = self._state.get_country_selected()
        country_label = make_label(country_selected, 'all countries')
        draw_select(x,  country_label, 'countries')

        x += 185
        category_selected = self._state.get_category_selected()
        category_label = make_label(category_selected, 'all categories')
        draw_select(x, category_label, 'categories')

        x += 185
        tag_selected = self._state.get_tag_selected()
        tag_label = make_label(tag_selected, 'all tags')
        draw_select(x, tag_label, 'tags')

        x += 185
        keyword_selected = self._state.get_keyword_selected()
        keyword_label = make_label(keyword_selected, 'all keywords')
        draw_select(x, keyword_label, 'keywords')

        # Draw button
        button_hover = self._button_hover == 'button'
        self._sketch.set_stroke(const.HOVER_COLOR if button_hover else const.INACTIVE_COLOR)
        self._sketch.set_fill(const.DARK_BG_COLOR if button_hover else const.DEEP_BG_COLOR)
        self._sketch.set_rect_mode('corner')
        self._sketch.draw_rect(
            const.BUTTON_X,
            const.BUTTON_Y,
            const.BUTTON_WIDTH - 1,
            const.BUTTON_HEIGHT
        )

        self._sketch.clear_stroke()
        self._sketch.set_fill(const.HOVER_COLOR if button_hover else const.INACTIVE_COLOR)
        self._sketch.set_text_align('center', 'baseline')
        self._sketch.set_text_font('IBMPlexMono-Regular.ttf', 14)
        self._sketch.draw_text(
            const.BUTTON_X + const.BUTTON_WIDTH / 2 - 1,
            text_y,
            self._get_button_text()
        )

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def _get_button_text(self) -> str:
        return {
            'overview': 'Go to Grid >',
            'grid': 'Go to Overview >'
        }.get(self._movement, 'Done >')


def main():
    visualization = NewsVisualization()
    visualization.show()


if __name__ == '__main__':
    main()
