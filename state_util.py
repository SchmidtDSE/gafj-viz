import data_util


class VizState:

    def __init__(self):
        self._country_selected: data_util.OPT_STR = None
        self._country_hovering: data_util.OPT_STR = None
        self._tag_selected: data_util.OPT_STR = None
        self._tag_hovering: data_util.OPT_STR = None
        self._keyword_selected: data_util.OPT_STR = None
        self._keyword_hovering: data_util.OPT_STR = None
    
    def set_country_selected(self, new_val: str):
        self._country_selected = new_val

    def get_country_selected(self) -> str:
        return self._country_selected

    def clear_country_selected(self):
        self._country_selected = None
    
    def set_country_hovering(self, new_val: str):
        self._country_hovering = new_val

    def get_country_hovering(self) -> str:
        return self._country_hovering

    def clear_country_hovering(self):
        self._country_hovering = None
    
    def set_tag_selected(self, new_val: str):
        self._tag_selected = new_val

    def get_tag_selected(self) -> str:
        return self._tag_selected

    def clear_tag_selected(self):
        self._tag_selected = None
    
    def set_tag_hovering(self, new_val: str):
        self._tag_hovering = new_val

    def get_tag_hovering(self) -> str:
        return self._tag_hovering

    def clear_tag_hovering(self):
        self._tag_hovering = None
    
    def set_keyword_selected(self, new_val: str):
        self._keyword_selected = new_val

    def get_keyword_selected(self) -> str:
        return self._keyword_selected

    def clear_keyword_selected(self):
        self._keyword_selected = None
    
    def set_keyword_hovering(self, new_val: str):
        self._keyword_hovering = new_val

    def get_keyword_hovering(self) -> str:
        return self._keyword_hovering

    def clear_keyword_hovering(self):
        self._keyword_hovering = None

    def get_query(self, category: str) -> data_util.Query:
        return data_util.Query(
            category,
            self._country_selected,
            self._tag_selected,
            self._keyword_selected
        )
