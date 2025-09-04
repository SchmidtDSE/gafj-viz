"""Visualization-wide constants and utility functions to support use of those constants.

License: BSD
"""

import os

WIDTH = 1225
HEIGHT = 750

BG_COLOR = '#FFFFFF'
BG_COLOR_LAYER = '#F9F9F9A0'
DEEP_BG_COLOR = '#F5F5F5'
DARK_BG_COLOR = '#2A2A2A'

COLUMN_WIDTH = 200
COLUMN_PADDING = 50

INACTIVE_COLOR = '#666666'
ACTIVE_COLOR = '#0B977E'
HOVER_COLOR = '#0A8570'

INACTIVE_COLOR_MAP = '#66666690'
ACTIVE_COLOR_MAP = '#0B977E90'
HOVER_COLOR_MAP = '#0A857090'

FOOTER_HEIGHT = 50

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 39
BUTTON_X = WIDTH - BUTTON_WIDTH
BUTTON_Y = HEIGHT - BUTTON_HEIGHT - 1
DOWNLOAD_X = WIDTH - BUTTON_WIDTH * 2 - 5
DOWNLOAD_Y = BUTTON_Y

SELECTOR_X = 0
SELECTOR_Y = BUTTON_Y
SELECTOR_WIDTH = WIDTH - (BUTTON_WIDTH + 5) * 2
SELECTOR_HEIGHT = BUTTON_HEIGHT + 2

FONT = os.path.join('third_party_web', 'IBMPlexMono-Regular.ttf')

REWRITES = {
    'people and society': 'people & society',
    'economy and industry': 'econ & industry',
    'food and materials': 'food & materials',
    'health and body': 'health & body',
    'environment and resources': 'env & resource'
}


def rewrite(target: str) -> str:
    """Intercept a string and rewrite if found in const.REWRITES.

    Args:
        target: The string to potentially rewrite.

    Returns:
        Rewritten string if intercepted or the original string if no rewrite available.
    """
    return REWRITES.get(target, target)


def get_color(selected: bool, hovering: bool) -> str:
    """Determine which color constant to use.

    Args:
        selected: Flag indicating if the element is statefully selected by the user. True if
            selected and False otherwise.
        hovering: Flag indicating if the user's cursor is hovering over the elment. True if hovering
            and False otherwise.

    Returns:
        Color to use
    """
    if hovering:
        return HOVER_COLOR
    elif selected:
        return ACTIVE_COLOR
    else:
        return INACTIVE_COLOR
