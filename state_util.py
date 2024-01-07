import typing

import data_util


class VizState:

    def __init__(self):
        self._category_selected: data_util.OPT_STR = None
        self._category_hovering: data_util.OPT_STR = None
        self._country_selected: data_util.OPT_STR = None
        self._country_hovering: data_util.OPT_STR = None
        self._tag_selected: data_util.OPT_STR = None
        self._tag_hovering: data_util.OPT_STR = None
        self._keyword_selected: data_util.OPT_STR = None
        self._keyword_hovering: data_util.OPT_STR = None

    def set_category_selected(self, new_val: str):
        self._category_selected = new_val

    def toggle_category_selected(self, new_val: str):
        if self._category_selected == new_val:
            self._category_selected = None
        else:
            self._category_selected = new_val

    def get_category_selected(self) -> typing.Optional[str]:
        return self._category_selected

    def clear_category_selected(self):
        self._category_selected = None

    def set_category_hovering(self, new_val: str):
        self._category_hovering = new_val

    def get_category_hovering(self) -> typing.Optional[str]:
        return self._category_hovering

    def clear_category_hovering(self):
        self._category_hovering = None
    
    def set_country_selected(self, new_val: str):
        self._country_selected = new_val

    def toggle_country_selected(self, new_val: str):
        if self._country_selected == new_val:
            self._country_selected = None
        else:
            self._country_selected = new_val

    def get_country_selected(self) -> typing.Optional[str]:
        return self._country_selected

    def clear_country_selected(self):
        self._country_selected = None
    
    def set_country_hovering(self, new_val: str):
        self._country_hovering = new_val

    def get_country_hovering(self) -> typing.Optional[str]:
        return self._country_hovering

    def clear_country_hovering(self):
        self._country_hovering = None
    
    def set_tag_selected(self, new_val: str):
        self._tag_selected = new_val

    def toggle_tag_selected(self, new_val: str):
        if self._tag_selected == new_val:
            self._tag_selected = None
        else:
            self._tag_selected = new_val

    def get_tag_selected(self) -> typing.Optional[str]:
        return self._tag_selected

    def clear_tag_selected(self):
        self._tag_selected = None
    
    def set_tag_hovering(self, new_val: str):
        self._tag_hovering = new_val

    def get_tag_hovering(self) -> typing.Optional[str]:
        return self._tag_hovering

    def clear_tag_hovering(self):
        self._tag_hovering = None
    
    def set_keyword_selected(self, new_val: str):
        self._keyword_selected = new_val

    def toggle_keyword_selected(self, new_val: str):
        if self._keyword_selected == new_val:
            self._keyword_selected = None
        else:
            self._keyword_selected = new_val

    def get_keyword_selected(self) -> typing.Optional[str]:
        return self._keyword_selected

    def clear_keyword_selected(self):
        self._keyword_selected = None
    
    def set_keyword_hovering(self, new_val: str):
        self._keyword_hovering = new_val

    def get_keyword_hovering(self) -> typing.Optional[str]:
        return self._keyword_hovering

    def clear_keyword_hovering(self):
        self._keyword_hovering = None

    def get_query(self, category: typing.Optional[str] = None) -> data_util.Query:
        return data_util.Query(
            category,
            self._category_selected,
            self._country_selected,
            self._tag_selected,
            self._keyword_selected
        )

    def serialize(self) -> str:
        pieces = [
            self._category_selected,
            self._category_hovering,
            self._country_selected,
            self._country_hovering,
            self._tag_selected,
            self._tag_hovering,
            self._keyword_selected,
            self._keyword_hovering
        ]
        return '\t'.join(map(lambda x: str(x), pieces))
