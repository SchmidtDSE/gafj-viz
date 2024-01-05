import typing

import sketchingpy

import data_util
import state_util

import const
import grid_viz


class NewsVisualization:

    def __init__(self):
        self._changed = True
        self._drawn = False
        self._state = state_util.VizState()
        self._sketch = sketchingpy.Sketch2D(1225, 900, 'News Visualization')
        self._sketch.set_fps(15)

        data_layer = self._sketch.get_data_layer()
        compressed_data = data_layer.get_text('serialized.txt')
        compressed_lines = compressed_data.split('\n')
        self._accessor = data_util.CompressedDataAccessor(compressed_lines)

        self._grid = grid_viz.GridViz(self._sketch, self._accessor, self._state)

        self._sketch.on_step(lambda sketch: self._draw())
        self._sketch.get_mouse().on_button_press(
            lambda button: self._respond_to_click()
        )

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
            
            self._grid.check_hover(mouse_x, mouse_y)

            self._changed = prior_state_str != self._state.serialize()

        if self._changed:
            self._sketch.clear(const.BG_COLOR)
            self._grid.draw()
            self._drawn = True
            self._changed = False

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def _respond_to_click(self):
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

        self._grid.refresh_data()

        self._changed = True
        self._drawn = False

    



def main():
    visualization = NewsVisualization()
    visualization.show()


if __name__ == '__main__':
    main()
