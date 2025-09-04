"""Visualization movement which previews individual article's metadata.

License: BSD
"""

import random

import sketchingpy

import abstract
import article_getter
import const
import data_util
import state_util


class ArticlePreviewViz(abstract.VizMovement):
    """Movement which shows title and other metadata previews of articles matching a query."""

    def __init__(self, sketch: sketchingpy.Sketch2D, accessor: data_util.DataAccessor,
        state: state_util.VizState):
        """Create a new instance of this movement.

        Args:
            sketch: The sketch in which this movement operates.
            accessor: Unused accessor which provides access to article aggregate statistics.
            state: Object describing the global visualization state modified by multiple movements.
        """
        self._sketch = sketch
        self._accessor = accessor
        self._state = state
        self._loading_drawn = False
        self._articles = None
        self._state_loaded = None
        self._locked = False

    def lock(self):
        """Have the visualization ignore inputs."""
        pass

    def unlock(self):
        """Have the visualization respond to inputs."""
        pass

    def check_state(self, mouse_x: float, mouse_y: float):
        """Refresh data if articles not loaded, otherwise noop."""
        if not self._articles:
            self.refresh_data()

    def draw(self):
        """Draw article list or a please wait message."""
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.set_rect_mode('corner')
        self._sketch.clear_stroke()
        self._sketch.set_fill(const.DEEP_BG_COLOR)
        self._sketch.draw_rect(0, 0, const.WIDTH, 50)

        self._sketch.set_text_font(const.FONT, 30)
        self._sketch.set_text_align('left', 'center')
        self._sketch.set_fill(const.INACTIVE_COLOR)
        self._sketch.draw_text(5, 25, 'Matching articles')

        if not self._loading_drawn:
            self._sketch.draw_text(5, 70, 'Please wait...')
            self._loading_drawn = True
            self._state.invalidate()
        elif self._articles:
            self._draw_articles_buffer()

        self._sketch.pop_style()
        self._sketch.pop_transform()

    def refresh_data(self):
        """Load underlying article metadata list if required."""
        if self._state_loaded == self._state.serialize():
            return

        if not self._loading_drawn:
            return

        params = {}

        def add_to_params(value, key):
            if value is None:
                return
            else:
                params[key] = value

        add_to_params(self._state.get_keyword_selected(), 'keyword')
        add_to_params(self._state.get_tag_selected(), 'tag')
        add_to_params(self._state.get_category_selected(), 'category')
        add_to_params(self._state.get_country_selected(), 'country')

        self._articles = article_getter.local_handler(params)
        random.shuffle(self._articles)

        self._state_loaded = self._state.serialize()
        self._state.invalidate()
        self._draw_articles()

    def on_change_to(self):
        """Prepare loading screen prior to first or invalidated cache draw."""
        self.refresh_data()
        self._loading_drawn = False

    def download_articles(self):
        """Produce a CSV export describing matching articles."""
        def callback(filename):
            if not filename.endswith('.csv'):
                filename = filename + '.csv'

            article_dicts = map(lambda x: x.to_dict(), self._articles)
            self._sketch.get_data_layer().write_csv(
                article_dicts,
                [
                    'url',
                    'titleOriginal',
                    'titleEnglish',
                    'published',
                    'country',
                    'keywordList',
                    'tagList',
                    'categoryList'
                ],
                filename
            )

        self._sketch.get_dialog_layer().get_file_save_location(callback)

    def _draw_articles_buffer(self):
        self._sketch.draw_buffer(0, 0, 'articles')

    def _draw_articles(self):
        self._sketch.push_transform()
        self._sketch.push_style()

        self._sketch.create_buffer('articles', const.WIDTH, const.HEIGHT)
        self._sketch.enter_buffer('articles')

        self._sketch.clear_stroke()
        self._sketch.set_text_font(const.FONT, 30)
        self._sketch.set_text_align('left', 'center')
        self._sketch.set_fill(const.INACTIVE_COLOR)
        self._sketch.draw_text(5, 25, 'Matching articles')

        y = 80
        for article in self._articles[:20]:
            self._sketch.set_text_font(const.FONT, 16)
            self._sketch.set_text_align('left', 'baseline')
            self._sketch.draw_text(5, y, article.get_title_english())

            text = ' | '.join([
                article.get_country(),
                article.get_published()[:10],
                article.get_url()
            ])

            self._sketch.set_text_font(const.FONT, 12)
            self._sketch.set_text_align('left', 'top')
            self._sketch.draw_text(5, y + 5, text)

            y += 45

        self._sketch.exit_buffer()

        self._sketch.pop_style()
        self._sketch.pop_transform()
