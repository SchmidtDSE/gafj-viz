"""Utilities for querying for article summary statistics.

Utilities for querying for and working with summary statistics which describe a collection of
Articles.

License: BSD
"""

import itertools
import typing

OPT_STR = typing.Optional[str]
PATH_DB = 'articles.db'
CATEGORIES = {
    'people and society',
    'economy and industry',
    'food and materials',
    'health and body',
    'environment and resources'
}


class Query:
    """Object describing a query for a set of articles to be summarized as statistics."""

    def __init__(self, category: OPT_STR, pre_category: OPT_STR, country: OPT_STR, tag: OPT_STR,
        keyword: OPT_STR):
        """Create a new query.

        Args:
            category: The database name for a category for which articles should be filtered. Pass
                None if all categories should be included.
            pre_category: The database name for a second category for which articles should be
                filtered prior to applying other filters. Pass None if all categories should be
                included.
            country: The database name for a country for which articles should be filtered. Pass
                None if all countries should be included.
            tag: The database name for a tag for which articles should be filtered. Pass None if all
                tags should be included.
            keyword: The database name for a keyword for which articles should be filtered. Pass
                None if all keywords should be included.
        """
        self._category = category
        self._pre_category = pre_category
        self._country = country
        self._tag = tag
        self._keyword = keyword

    def has_category(self) -> bool:
        """Determine if this query has a category for which articles should be filtered.

        Returns:
            True if there is a category filter and False otherwise.
        """
        return self._category is not None

    def get_category(self) -> OPT_STR:
        """Get the potential category for which this query filters.

        Returns:
            The database name for a category for which articles should be filtered. Will be None if
            all categories should be included.
        """
        return self._category

    def has_pre_category(self) -> bool:
        """Determine if this query has a second category for which articles should be pre-filtered.

        Returns:
            True if there is a category pre-filter and False otherwise.
        """
        return self._pre_category is not None

    def get_pre_category(self) -> OPT_STR:
        """Get the potential category for which this query pre-filters.

        Returns:
            The database name for a category for which articles should be pre-filtered. Will be None
            if all categories should be included.
        """
        return self._pre_category

    def has_country(self) -> bool:
        """Determine if this query has a country for which articles should be filtered.

        Returns:
            True if there is a country filter and False otherwise.
        """
        return self._country is not None

    def get_country(self) -> OPT_STR:
        """Get the potential country for which this query filters.

        Returns:
            The database name for a country for which articles should be filtered. Will be None if
            all countries should be included.
        """
        return self._country

    def has_tag(self) -> bool:
        """Determine if this query has a tag for which articles should be filtered.

        Returns:
            True if there is a tag filter and False otherwise.
        """
        return self._tag is not None

    def get_tag(self) -> OPT_STR:
        """Get the potential tag for which this query filters.

        Returns:
            The database name for a tag for which articles should be filtered. Will be None if
            all tags should be included.
        """
        return self._tag

    def has_keyword(self) -> bool:
        """Determine if this query has a keyword for which articles should be filtered.

        Returns:
            True if there is a keyword filter and False otherwise.
        """
        return self._keyword is not None

    def get_keyword(self) -> OPT_STR:
        """Get the potential keyword for which this query filters.

        Returns:
            The database name for a keyword for which articles should be filtered. Will be None if
            all keywords should be included.
        """
        return self._keyword

    def get_has_filters(self) -> bool:
        """Determine if this query has any filters.

        Returns:
            True if this query has some filters and False if this query has no filters and all
            articles will be returned.
        """
        all_flags = [
            self.has_pre_category(),
            self.has_country(),
            self.has_tag(),
            self.has_keyword()
        ]
        return sum(map(lambda x: 1 if x else 0, all_flags)) > 0

    def get_id_str(self) -> str:
        """Get a string serialization of this query.

        Returns:
            String representing this query such that, if two queries have the same string, they
            execute functionally the same query.
        """
        components = [
            self._category,
            self._pre_category,
            self._country,
            self._tag,
            self._keyword
        ]
        components_str = map(lambda x: str(x), components)
        return '\t'.join(components_str)


class CountedGroup:
    """Object representing a group of articles where articles may be in multiple groups."""

    def __init__(self, name: str, count: int):
        """Create a new record of a group of articles.

        Args:
            name: Get the name which identifies a common attribute of of all of the articles in this
                group.
            count: The number of articles in this group.
        """
        self._name = name
        self._count = count

    def get_name(self) -> str:
        """Get a description of a common attribute of articles in this group.
        
        Returns:
            A string name which identifies a common attribute of of all of the articles in this
            group.
        """
        return self._name

    def get_count(self) -> int:
        """Get the size of this group.

        Returns:
            The number of articles in this group.
        """
        return self._count


COUNTED_GROUPS = typing.List[CountedGroup]


class Country:
    """Object describing a country found within this dataset."""

    def __init__(self, name: str):
        """Create a new record of a country.

        Args:
            name: The human readable name of the country.
        """
        self._name = name

    def get_name(self) -> str:
        """Get the unique name of this country.

        Returns:
            The human readable name of the country.
        """
        return self._name


class Category:
    """Category or top level categorization within the topic model."""

    def __init__(self, name: str):
        """Create a record of a new category.

        Args:
            name: The human readable but unique name of this category.
        """
        self._name = name

    def get_name(self) -> str:
        """Get the unique string ID associated with this category.

        Returns:
            The human readable but unique name of this category.
        """
        return self._name


class Result:
    """A group of articles found as result of executing a query."""

    def __init__(self, total_count: int, group_count: int, categories: COUNTED_GROUPS,
        countries: COUNTED_GROUPS, country_totals: COUNTED_GROUPS, tags: COUNTED_GROUPS,
        keywords: COUNTED_GROUPS, has_filters: bool):
        """Create a record of a query result.

        Args:
            total_count: The number of articles from which this group was drawn (from which they
                were queried).
            group_count: The number of articles in this group.
            categories: The categories in which these articles are found.
            countries: The countries in which these articles are found.
            country_totals: Mapping from country to the number of all articles in the target
                population found in that country regardless of if they satisfy the query's filters.
            tags: The tags with which these articles are associated.
            keywords: The keywords with which these articles are associated.
            has_filters: Flag indicating if the query used to generate these results had any
                filters. True if the query had filters and false if it had no filters and all of the
                population is in this result.
        """
        self._total_count = total_count
        self._group_count = group_count
        self._categories = categories
        self._countries = countries
        self._country_totals = country_totals
        self._tags = tags
        self._keywords = keywords
        self._has_filters = has_filters

    def get_total_count(self) -> int:
        """Get the number of articles in the population from which these articles were queried.

        Returns:
            The number of articles from which this group was drawn (from which they were queried).
        """
        return self._total_count

    def get_group_count(self) -> int:
        """Get the number of articles matching the query.

        Returns:
            The number of articles in this group.
        """
        return self._group_count

    def get_categories(self) -> COUNTED_GROUPS:
        """Get the categories with which these query results are associated in the topic model.

        Returns:
            The categories in which these articles are found.
        """
        return self._categories

    def get_countries(self) -> COUNTED_GROUPS:
        """Get the countries with which these query results are associated.

        Returns:
            The countries in which these articles are found.
        """
        return self._countries

    def get_country_totals(self) -> COUNTED_GROUPS:
        """Get the total number of articles per country from which these results were queried.

        Returns:
            Mapping from country to the number of all articles in the target population found in
            that country regardless of if they satisfy the query's filters.
        """
        return self._country_totals

    def get_tags(self) -> COUNTED_GROUPS:
        """Get the tags with which these query results are associated in the topic model.

        Returns:
            The tags with which these articles are associated.
        """
        return self._tags

    def get_keywords(self) -> COUNTED_GROUPS:
        """Get the keywords with which these query results are associated in the topic model.

        Returns:
            The keywords with which these articles are associated.
        """
        return self._keywords

    def get_has_filters(self) -> bool:
        """Determine if the query that generated these results had a filters.

        Returns:
            Flag indicating if the query used to generate these results had any filters. True if the
            query had filters and false if it had no filters and all of the population is in this
            result.
        """
        return self._has_filters


class Tag:
    """Object representing a tag in the topic model."""

    def __init__(self, name: str, category: Category):
        """Create a new record of a tag.

        Args:
            name: Unique but human-readable string representing this tag.
            category: The category in which this tag is a member.
        """
        self._name = name
        self._category = category

    def get_name(self) -> str:
        """Get the unique string identifier for this tag.

        Returns:
            Unique but human-readable string representing this tag.
        """
        return self._name

    def get_category(self) -> Category:
        """Get the category in which this tag is found.

        Returns:
            The category in which this tag is a member.
        """
        return self._category


class Keyword:
    """Object representing a keyword in the topic model."""

    def __init__(self, name: str, category: Category, tag: Tag):
        """Create a new record of a keyword.

        Args:
            name: Unique but human-readable string representing this keyword as found in articles.
            category: The category in which this keyword is a member.
            tag: The tag in which this keyword is a member.
        """
        self._name = name
        self._category = category
        self._tag = tag

    def get_name(self) -> str:
        """Get a unique string describing this keyword.

        Returns:
            Unique but human-readable string representing this keyword as found in articles.
        """
        return self._name

    def get_category(self) -> Category:
        """Get the category in which this keyword is member.

        Returns:
            The category in which this keyword is a member.
        """
        return self._category

    def get_tag(self) -> Tag:
        """Get the tag in which this keyword is member.

        Returns:
            The tag in which this keyword is a member.
        """
        return self._tag


class ArticleSet:
    """Object representing a collection of articles with identical topical metadata.

    Object representing a collection of articles with identical topical metadata in that they all
    see the same results in the topic model and are associated to the same country.
    """

    def __init__(self, country: Country, categories: typing.List[Category], tags: typing.List[Tag],
        keywords: typing.List[Keyword], count: int):
        """Create a new record of a set of articles with identical results in the topical model.

        Args:
            country: The country where all of these articles are found.
            categories: List of categories in which all of these articles are members.
            tags: List of tags in which all of these articles are members.
            keywords: List of keywords in which all of these articles are members.
            count: Number of articles in this set.
        """
        self._country = country
        self._categories = categories
        self._tags = tags
        self._keywords = keywords
        self._count = count

    def get_country(self) -> Country:
        """Get the country where all of these articles are found.

        Returns:
            The country where all of these articles are found.
        """
        return self._country

    def get_categories(self) -> typing.List[Category]:
        """Get the categories for all of these articles.

        Returns:
            List of categories in which all of these articles are members.
        """
        return self._categories

    def has_category(self, name: str) -> bool:
        """Determine if these articles are part of a category.

        Args:
            name: The unique string identifier for the category.

        Returns:
            True if all articles in this set are part of the given category or False otherwise.
        """
        return self._check_for(name, self._categories)

    def get_tags(self) -> typing.List[Tag]:
        """Get the tags for all of these articles.

        Returns:
            List of tags in which all of these articles are members.
        """
        return self._tags

    def has_tag(self, name: str) -> bool:
        """Determine if these articles are part of a tag.

        Args:
            name: The unique string identifier for the tag.

        Returns:
            True if all articles in this set are part of the given tag or False otherwise.
        """
        return self._check_for(name, self._tags)

    def get_keywords(self) -> typing.List[Keyword]:
        """Get the keywords for all of these articles.

        Returns:
            List of keywords in which all of these articles are members.
        """
        return self._keywords

    def has_keyword(self, name: str) -> bool:
        """Determine if these articles have a keyword.

        Args:
            name: The unique string identifier for the keyword.

        Returns:
            True if all articles in this set have a keyword or False otherwise.
        """
        return self._check_for(name, self._keywords)

    def get_count(self) -> int:
        """Get the size of this group.

        Returns:
            The count of articles in this set.
        """
        return self._count

    def _check_for(self, name: str, target) -> bool:
        names = map(lambda x: x.get_name(), target)
        matched = filter(lambda x: x == name, names)
        count = sum(map(lambda x: 1, matched))
        return count > 0


class DataAccessor:
    """Interface for a strategy to query for article statistics."""

    def execute_query(self, query: Query) -> Result:
        """Execute a query and return aggregate statistics for the resulting set.

        Args:
            query: The query to execute.

        Returns:
            Result object describing summary statistics of the result set for the given query.
        """
        raise RuntimeError('Use implementor.')


class CompressedDataAccessor(DataAccessor):
    """Data accessor which queries inside a file using a custom compressed article format."""

    def __init__(self, contents: typing.Iterable[str]):
        """Create a new accessor around contents of a compressed file.

        Args:
            contents: The string lines of the compressed file.
        """
        self._countries: typing.Dict[int, Country] = {}
        self._categories: typing.Dict[int, Category] = {}
        self._tags: typing.Dict[int, Tag] = {}
        self._keywords: typing.Dict[int, Keyword] = {}
        self._articles: typing.List[ArticleSet] = []

        self._last_query_str = ''
        self._last_result: typing.Optional[Result] = None

        strategies = {
            'n': lambda x: self._load_country(x),
            'c': lambda x: self._load_category(x),
            't': lambda x: self._load_tag(x),
            'k': lambda x: self._load_keyword(x),
            'a': lambda x: self._load_article_set(x)
        }

        for line in contents:
            command = line[0]
            strategy = strategies[command]
            strategy(line)

    def execute_query(self, query: Query) -> Result:
        id_str = query.get_id_str()
        if self._last_query_str == id_str:
            assert self._last_result is not None
            return self._last_result

        addressable = self._get_addressable(query)
        total_count = self._get_total_count(addressable)
        by_country = self._get_by_country(self._articles)

        category = query.get_category()
        group_count = self._get_total_count_in_category(addressable, category)
        countries = self._get_by_country_in_category(addressable, category)
        categories = self._get_categories_in_category(addressable, category)
        tags = self._get_tags_in_category(addressable, category)
        keywords = self._get_keywords_in_category(addressable, category)

        new_result = Result(
            total_count,
            group_count,
            categories,
            countries,
            by_country,
            tags,
            keywords,
            query.get_has_filters()
        )

        self._last_query_str = id_str
        self._last_result = new_result

        return new_result

    def _get_addressable(self, query: Query) -> typing.List[ArticleSet]:
        addressable_group: typing.Iterable[ArticleSet] = self._articles

        if query.has_country():
            target_country = query.get_country()
            addressable_group = filter(
                lambda article: article.get_country().get_name() == target_country,
                addressable_group
            )

        if query.has_pre_category():
            target_category = query.get_pre_category()
            addressable_group = filter(
                lambda article: article.has_category(target_category),  # type: ignore
                addressable_group
            )

        if query.has_tag():
            target_tag = query.get_tag()
            addressable_group = filter(
                lambda article: article.has_tag(target_tag),  # type: ignore
                addressable_group
            )

        if query.has_keyword():
            target_keyword = query.get_keyword()
            addressable_group = filter(
                lambda article: article.has_keyword(target_keyword),  # type: ignore
                addressable_group
            )

        return list(addressable_group)

    def _get_total_count(self, target: typing.List[ArticleSet]) -> int:
        return sum(map(lambda x: x.get_count(), target))

    def _get_by_country(self, target: typing.Iterable[ArticleSet]) -> COUNTED_GROUPS:
        ret_counts: typing.Dict[str, int] = {}

        for article in target:
            country = article.get_country().get_name()
            count = article.get_count()
            ret_counts[country] = ret_counts.get(country, 0) + count

        return self._convert_dict_to_counted_groups(ret_counts)

    def _get_total_count_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> int:

        in_category: typing.Iterable[ArticleSet] = target
        if category:
            in_category = filter(lambda x: x.has_category(category), target)

        counts = map(lambda x: x.get_count(), in_category)
        return sum(counts)

    def _get_by_country_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> COUNTED_GROUPS:

        in_category: typing.Iterable[ArticleSet] = target
        if category:
            in_category = filter(lambda x: x.has_category(category), target)

        return self._get_by_country(in_category)

    def _get_categories_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> COUNTED_GROUPS:

        in_category: typing.Iterable[ArticleSet] = target
        if category:
            in_category = filter(lambda x: x.has_category(category), target)

        nested_categories = map(
            lambda x: self._propogate_count(x.get_categories(), x.get_count()),
            in_category
        )
        categories = itertools.chain(*nested_categories)
        return self._make_counts_from_flat(categories)

    def _get_tags_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> COUNTED_GROUPS:

        in_category: typing.Iterable[ArticleSet] = target
        if category:
            in_category = filter(lambda x: x.has_category(category), target)

        nested_tags = map(
            lambda x: self._propogate_count(x.get_tags(), x.get_count()),
            in_category
        )
        tags = itertools.chain(*nested_tags)

        tags_allowed: typing.Iterable = tags
        if category:
            tags_allowed = filter(
                lambda x: x[0].get_category().get_name() == category,
                tags
            )

        return self._make_counts_from_flat(tags_allowed)

    def _get_keywords_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> COUNTED_GROUPS:

        in_category: typing.Iterable[ArticleSet] = target
        if category:
            in_category = filter(lambda x: x.has_category(category), target)

        nested_keywords = map(
            lambda x: self._propogate_count(x.get_keywords(), x.get_count()),
            in_category
        )
        keywords = itertools.chain(*nested_keywords)

        keywords_allowed: typing.Iterable = keywords
        if category:
            keywords_allowed = filter(
                lambda x: x[0].get_tag().get_category().get_name() == category,
                keywords
            )

        return self._make_counts_from_flat(keywords_allowed)

    def _propogate_count(self, targets, count):
        return map(lambda x: (x, count), targets)

    def _make_counts_from_flat(self, obj_tuples) -> COUNTED_GROUPS:
        str_tuples = map(lambda x: (x[0].get_name(), x[1]), obj_tuples)

        ret_counts: typing.Dict[str, int] = {}
        for name, count in str_tuples:
            ret_counts[name] = ret_counts.get(name, 0) + count

        return self._convert_dict_to_counted_groups(ret_counts)

    def _convert_dict_to_counted_groups(self, target: typing.Dict[str, int]) -> COUNTED_GROUPS:
        objs = map(lambda x: CountedGroup(x[0], x[1]), target.items())
        return sorted(objs, key=lambda x: x.get_count(), reverse=True)

    def _load_country(self, line: str):
        pieces = line.split(' ')
        new_id = int(pieces[1])
        name = (' '.join(pieces[2:]))[1:-1]
        self._countries[new_id] = Country(name)

    def _load_category(self, line: str):
        pieces = line.split(' ')
        new_id = int(pieces[1])
        name = (' '.join(pieces[2:]))[1:-1]
        self._categories[new_id] = Category(name)

    def _load_tag(self, line: str):
        pieces = line.split(' ')
        category_id = int(pieces[1])
        tag_id = int(pieces[2])

        name = (' '.join(pieces[3:]))[1:-1]
        category = self._categories[category_id]

        self._tags[tag_id] = Tag(name, category)

    def _load_keyword(self, line: str):
        pieces = line.split(' ')
        category_id = int(pieces[1])
        tag_id = int(pieces[2])
        keyword_id = int(pieces[3])

        name = (' '.join(pieces[4:]))[1:-1]
        category = self._categories[category_id]
        tag = self._tags[tag_id]

        self._keywords[keyword_id] = Keyword(name, category, tag)

    def _load_article_set(self, line: str):
        def load_id_list(target: str) -> typing.List[int]:
            id_strs = target.split(';')
            id_ints = map(lambda x: int(x), id_strs)
            id_ints_allowed = filter(lambda x: x != -1, id_ints)
            return list(id_ints_allowed)

        pieces = line.split(' ')
        country_id = int(pieces[1])
        category_ids = load_id_list(pieces[2])
        tag_ids = load_id_list(pieces[3])
        keyword_ids = load_id_list(pieces[4])
        count = int(pieces[5])

        country = self._countries[country_id]
        categories = [self._categories[x] for x in category_ids]
        tags = [self._tags[x] for x in tag_ids]
        keywords = [self._keywords[x] for x in keyword_ids]

        new_article_set = ArticleSet(country, categories, tags, keywords, count)
        self._articles.append(new_article_set)
