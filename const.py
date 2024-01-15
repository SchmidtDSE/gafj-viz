WIDTH = 1225
HEIGHT = 900

BG_COLOR = '#505050'
BG_COLOR_LAYER = '#505050A0'
DEEP_BG_COLOR = '#303030C0'
DARK_BG_COLOR = '#303030'

COLUMN_WIDTH = 200
COLUMN_PADDING = 50

INACTIVE_COLOR = '#D0D0D0'
ACTIVE_COLOR = '#B2DF8A'
HOVER_COLOR = '#FFFFFF'

INACTIVE_COLOR_MAP = '#D0D0D090'
ACTIVE_COLOR_MAP = '#B2DF8A90'
HOVER_COLOR_MAP = '#FFFFFF90'

FOOTER_HEIGHT = 50

BUTTON_WIDTH = 200
BUTTON_HEIGHT = 39
BUTTON_X = WIDTH - BUTTON_WIDTH
BUTTON_Y = HEIGHT - BUTTON_HEIGHT
DOWNLOAD_X = WIDTH - BUTTON_WIDTH * 2 - 5
DOWNLOAD_Y = BUTTON_Y

SELECTOR_X = 0
SELECTOR_Y = BUTTON_Y
SELECTOR_WIDTH = WIDTH - (BUTTON_WIDTH + 5) * 2
SELECTOR_HEIGHT = BUTTON_HEIGHT

REWRITES = {
    'people and society': 'people & society',
    'economy and industry': 'econ & industry',
    'food and materials': 'food & materials',
    'health and body': 'health & body',
    'environment and resources': 'env & resource'
}


def get_color(selected: bool, hovering: bool) -> str:
    if hovering:
        return HOVER_COLOR
    elif selected:
        return ACTIVE_COLOR
    else:
        return INACTIVE_COLOR
