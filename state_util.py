"""Structure to represent global visualization state.

License: BSD
"""

import typing

import data_util


class VizState:
    """Global visualization state object tracking selected and hovering values."""

    def __init__(self):
        """Create a new state with nothing hovering or selected."""
        self._category_selected = None
        self._category_hovering = None
        self._country_selected = None
        self._country_hovering = None
        self._tag_selected = None
        self._tag_hovering = None
        self._keyword_selected = None
        self._keyword_hovering = None
        self._invalidation_id = 1

    def set_category_selected(self, new_val: str):
        """Set the filter value for category.

        Args:
            new_val: The value for which to filter.
        """
        self._category_selected = new_val

    def toggle_category_selected(self, new_val: str):
        """Set the filter value for category or, if new val equals current, it will be set to None.

        Args:
            new_val: The value for which to filter.
        """
        if self._category_selected == new_val:
            self._category_selected = None
        else:
            self._category_selected = new_val

    def get_category_selected(self) -> typing.Optional[str]:
        """Get the value of the current category filter.

        Returns:
            The category value for which the viz should filter or None if no filter is applied.
        """
        return self._category_selected

    def clear_category_selected(self):
        """Clear the category filter so that all categories are included in results."""
        self._category_selected = None

    def set_category_hovering(self, new_val: str):
        """Indicate which category over which the cursor is hovering.

        Args:
            new_val: The name of the group being hovered.
        """
        self._category_hovering = new_val

    def get_category_hovering(self) -> typing.Optional[str]:
        """Get the category over which the cursor is hovering.

        Returns:
            The category over which the cursor is hovering or None if no category is being hovered.
        """
        return self._category_hovering

    def clear_category_hovering(self):
        """Indicate that the cursor it not hovering over any category."""
        self._category_hovering = None

    def set_country_selected(self, new_val: str):
        """Set the filter value for coountry.

        Args:
            new_val: The value for which to filter.
        """
        self._country_selected = new_val

    def toggle_country_selected(self, new_val: str):
        """Set the filter value for country or, if new val equals current, it will be set to None.

        Args:
            new_val: The value for which to filter.
        """
        if self._country_selected == new_val:
            self._country_selected = None
        else:
            self._country_selected = new_val

    def get_country_selected(self) -> typing.Optional[str]:
        """Get the value of the current country filter.

        Returns:
            The country value for which the viz should filter or None if no filter is applied.
        """
        return self._country_selected

    def clear_country_selected(self):
        """Clear the country filter so that all countries are included in results."""
        self._country_selected = None

    def set_country_hovering(self, new_val: str):
        """Indicate which country over which the cursor is hovering.

        Args:
            new_val: The name of the group being hovered.
        """
        self._country_hovering = new_val

    def get_country_hovering(self) -> typing.Optional[str]:
        """Get the country over which the cursor is hovering.

        Returns:
            The country over which the cursor is hovering or None if no country is being hovered.
        """
        return self._country_hovering

    def clear_country_hovering(self):
        """Indicate that the cursor it not hovering over any country."""
        self._country_hovering = None

    def set_tag_selected(self, new_val: str):
        """Set the filter value for tag.

        Args:
            new_val: The value for which to filter.
        """
        self._tag_selected = new_val

    def toggle_tag_selected(self, new_val: str):
        """Set the filter value for tag or, if new val equals current, it will be set to None.

        Args:
            new_val: The value for which to filter.
        """
        if self._tag_selected == new_val:
            self._tag_selected = None
        else:
            self._tag_selected = new_val

    def get_tag_selected(self) -> typing.Optional[str]:
        """Get the value of the current tag filter.

        Returns:
            The tag value for which the viz should filter or None if no filter is applied.
        """
        return self._tag_selected

    def clear_tag_selected(self):
        """Clear the tag filter so that all tags are included in results."""
        self._tag_selected = None

    def set_tag_hovering(self, new_val: str):
        """Indicate which tag over which the cursor is hovering.

        Args:
            new_val: The name of the group being hovered.
        """
        self._tag_hovering = new_val

    def get_tag_hovering(self) -> typing.Optional[str]:
        """Get the tag over which the cursor is hovering.

        Returns:
            The tag over which the cursor is hovering or None if no tag is being hovered.
        """
        return self._tag_hovering

    def clear_tag_hovering(self):
        """Indicate that the cursor it not hovering over any tag."""
        self._tag_hovering = None

    def set_keyword_selected(self, new_val: str):
        """Set the filter value for keyword.

        Args:
            new_val: The value for which to filter.
        """
        self._keyword_selected = new_val

    def toggle_keyword_selected(self, new_val: str):
        """Set the filter value for keyword or, if new val equals current, it will be set to None.

        Args:
            new_val: The value for which to filter.
        """
        if self._keyword_selected == new_val:
            self._keyword_selected = None
        else:
            self._keyword_selected = new_val

    def get_keyword_selected(self) -> typing.Optional[str]:
        """Get the value of the current keyword filter.

        Returns:
            The keyword value for which the viz should filter or None if no filter is applied.
        """
        return self._keyword_selected

    def clear_keyword_selected(self):
        """Clear the keyword filter so that all keywords are included in results."""
        self._keyword_selected = None

    def set_keyword_hovering(self, new_val: str):
        """Indicate which keyword over which the cursor is hovering.

        Args:
            new_val: The name of the group being hovered.
        """
        self._keyword_hovering = new_val

    def get_keyword_hovering(self) -> typing.Optional[str]:
        """Get the keyword over which the cursor is hovering.

        Returns:
            The keyword over which the cursor is hovering or None if no keyword is being hovered.
        """
        return self._keyword_hovering

    def clear_keyword_hovering(self):
        """Indicate that the cursor it not hovering over any keyword."""
        self._keyword_hovering = None

    def invalidate(self):
        """Increment the validation ID such taht the serialization is different."""
        self._invalidation_id += 1

    def get_query(self, category: typing.Optional[str] = None) -> data_util.Query:
        """Create a query with the same filters as those currently active in this state.

        Args:
            category: The second category on which to filter or None if no second category filter
                should be applied. Defaults to None.

        Returns:
            Newly created Query.
        """
        return data_util.Query(
            category,
            self._category_selected,
            self._country_selected,
            self._tag_selected,
            self._keyword_selected
        )

    def serialize(self) -> str:
        """Create a string identifying this state.

        Returns:
            A string with a snapshot of the visualization state including both hovering and selected
            values. If two state objects have the same serialization they are functionally the same.
            Note that this also includes an invalidation ID such that two states with different
            invalidation counts are not treated as the same state.
        """
        pieces = [
            self._category_selected,
            self._category_hovering,
            self._country_selected,
            self._country_hovering,
            self._tag_selected,
            self._tag_hovering,
            self._keyword_selected,
            self._keyword_hovering,
            str(self._invalidation_id)
        ]
        return '\t'.join(map(lambda x: str(x), pieces))
