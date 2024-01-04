BG_COLOR = '#505050'
BG_COLOR_LAYER = '#505050A0'
DEEP_BG_COLOR = '#303030C0'

COLUMN_WIDTH = 200
COLUMN_PADDING = 50

INACTIVE_COLOR = '#D0D0D0'
ACTIVE_COLOR = '#B2DF8A'
HOVER_COLOR = '#FFFFFF'

REWRITES = {
    'people and society': 'people & society',
    'economy and industry': 'econ & industry',
    'food and materials': 'food & materials',
    'health and body': 'health & body',
    'environment and resources': 'env & resource'
}


def get_color(selected: bool, hovering: bool) -> str:
    if selected:
        return ACTIVE_COLOR
    elif hovering:
        return HOVER_COLOR
    else:
        return INACTIVE_COLOR
