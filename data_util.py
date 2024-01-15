import itertools
import os
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

    def __init__(self, category: OPT_STR, pre_category: OPT_STR, country: OPT_STR, tag: OPT_STR,
        keyword: OPT_STR):
        self._category = category
        self._pre_category = pre_category
        self._country = country
        self._tag = tag
        self._keyword = keyword

    def has_category(self) -> bool:
        return self._category is not None

    def get_category(self) -> OPT_STR:
        return self._category

    def has_pre_category(self) -> bool:
        return self._pre_category is not None 

    def get_pre_category(self) -> OPT_STR:
        return self._pre_category

    def has_country(self) -> bool:
        return self._country is not None

    def get_country(self) -> OPT_STR:
        return self._country

    def has_tag(self) -> bool:
        return self._tag is not None

    def get_tag(self) -> OPT_STR:
        return self._tag

    def has_keyword(self) -> bool:
        return self._keyword is not None

    def get_keyword(self) -> OPT_STR:
        return self._keyword

    def get_has_filters(self) -> bool:
        all_flags = [
            self.has_pre_category(),
            self.has_country(),
            self.has_tag(),
            self.has_keyword()
        ]
        return sum(map(lambda x: 1 if x else 0, all_flags)) > 0

    def get_id_str(self) -> str:
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

    def __init__(self, name: str, count: int):
        self._name = name
        self._count = count

    def get_name(self) -> str:
        return self._name

    def get_count(self) -> int:
        return self._count


COUNTED_GROUPS = typing.List[CountedGroup]


class Country:

    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name


class Category:

    def __init__(self, name: str):
        self._name = name

    def get_name(self) -> str:
        return self._name


class Result:

    def __init__(self, total_count: int, group_count: int, categories: COUNTED_GROUPS,
        countries: COUNTED_GROUPS, country_totals: COUNTED_GROUPS, tags: COUNTED_GROUPS,
        keywords: COUNTED_GROUPS, has_filters: bool):
        self._total_count = total_count
        self._group_count = group_count
        self._categories = categories
        self._countries = countries
        self._country_totals = country_totals
        self._tags = tags
        self._keywords = keywords
        self._has_filters = has_filters

    def get_total_count(self) -> int:
        return self._total_count

    def get_group_count(self) -> int:
        return self._group_count

    def get_categories(self) -> COUNTED_GROUPS:
        return self._categories

    def get_countries(self) -> COUNTED_GROUPS:
        return self._countries

    def get_country_totals(self) -> COUNTED_GROUPS:
        return self._country_totals

    def get_tags(self) -> COUNTED_GROUPS:
        return self._tags

    def get_keywords(self) -> COUNTED_GROUPS:
        return self._keywords

    def get_has_filters(self) -> bool:
        return self._has_filters


class Tag:

    def __init__(self, name: str, category: Category):
        self._name = name
        self._category = category

    def get_name(self) -> str:
        return self._name

    def get_category(self) -> Category:
        return self._category


class Keyword:

    def __init__(self, name: str, category: Category, tag: Tag):
        self._name = name
        self._category = category
        self._tag = tag

    def get_name(self) -> str:
        return self._name

    def get_category(self) -> Category:
        return self._category

    def get_tag(self) -> Tag:
        return self._tag


class ArticleSet:

    def __init__(self, country: Country, categories: typing.List[Category], tags: typing.List[Tag],
        keywords: typing.List[Keyword], count: int):
        self._country = country
        self._categories = categories
        self._tags = tags
        self._keywords = keywords
        self._count = count
    
    def get_country(self) -> Country:
        return self._country
    
    def get_categories(self) -> typing.List[Category]:
        return self._categories

    def has_category(self, name: str) -> bool:
        return self._check_for(name, self._categories)
    
    def get_tags(self) -> typing.List[Tag]:
        return self._tags

    def has_tag(self, name: str) -> bool:
        return self._check_for(name, self._tags)
    
    def get_keywords(self) -> typing.List[Keyword]:
        return self._keywords

    def has_keyword(self, name: str) -> bool:
        return self._check_for(name, self._keywords)
    
    def get_count(self) -> int:
        return self._count

    def _check_for(self, name: str, target) -> bool:
        names = map(lambda x: x.get_name(), target)
        matched = filter(lambda x: x == name, names)
        count = sum(map(lambda x: 1, matched))
        return count > 0


class DataAccessor:

    def execute_query(self, query: Query) -> Result:
        raise RuntimeError('Use implementor.')


class CompressedDataAccessor(DataAccessor):

    def __init__(self, contents: typing.Iterable[str]):
        self._countries: typing.Dict[int, Country] = {}
        self._categories: typing.Dict[int, Category] = {}
        self._tags: typing.Dict[int, Tag] = {}
        self._keywords: typing.Dict[int, Keyword] = {}
        self._articles: typing.List[ArticleSet] = []
        
        self._last_query_str = ''
        self._last_result = None

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
        addressable_group = self._articles

        if query.has_country():
            target_country = query.get_country()
            addressable_group = filter(
                lambda article: article.get_country().get_name() == target_country,
                addressable_group
            )

        if query.has_pre_category():
            target_category = query.get_pre_category()
            addressable_group = filter(
                lambda article: article.has_category(target_category),
                addressable_group
            )

        if query.has_tag():
            target_tag = query.get_tag()
            addressable_group = filter(
                lambda article: article.has_tag(target_tag),
                addressable_group
            )

        if query.has_keyword():
            target_keyword = query.get_keyword()
            addressable_group = filter(
                lambda article: article.has_keyword(target_keyword),
                addressable_group
            )

        return list(addressable_group)

    def _get_total_count(self, target: typing.List[ArticleSet]) -> int:
        return sum(map(lambda x: x.get_count(), target))

    def _get_by_country(self, target: typing.Iterable[ArticleSet]) -> COUNTED_GROUPS:
        ret_counts = {}

        for article in target:
            country = article.get_country().get_name()
            count = article.get_count()
            ret_counts[country] = ret_counts.get(country, 0) + count

        return self._convert_dict_to_counted_groups(ret_counts)

    def _get_total_count_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> typing.List[ArticleSet]:
        
        if category:
            in_category = filter(lambda x: x.has_category(category), target)
        else:
            in_category = target
        
        counts = map(lambda x: x.get_count(), in_category)
        return sum(counts)

    def _get_by_country_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> typing.List[ArticleSet]:

        if category:
            in_category = filter(lambda x: x.has_category(category), target)
        else:
            in_category = target

        return self._get_by_country(in_category)

    def _get_categories_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> typing.List[ArticleSet]:

        if category:
            in_category = filter(lambda x: x.has_category(category), target)
        else:
            in_category = target

        nested_categories = map(
            lambda x: self._propogate_count(x.get_categories(), x.get_count()),
            in_category
        )
        categories = itertools.chain(*nested_categories)
        return self._make_counts_from_flat(categories)

    def _get_tags_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> typing.List[ArticleSet]:

        if category:
            in_category = filter(lambda x: x.has_category(category), target)
        else:
            in_category = target

        nested_tags = map(
            lambda x: self._propogate_count(x.get_tags(), x.get_count()),
            in_category
        )
        tags = itertools.chain(*nested_tags)

        if category:
            tags_allowed = filter(
                lambda x: x[0].get_category().get_name() == category,
                tags
            )
        else:
            tags_allowed = tags

        return self._make_counts_from_flat(tags_allowed)

    def _get_keywords_in_category(self, target: typing.List[ArticleSet],
        category: OPT_STR) -> typing.List[ArticleSet]:

        if category:
            in_category = filter(lambda x: x.has_category(category), target)
        else:
            in_category = target

        nested_keywords = map(
            lambda x: self._propogate_count(x.get_keywords(), x.get_count()),
            in_category
        )
        keywords = itertools.chain(*nested_keywords)

        if category:
            keywords_allowed = filter(
                lambda x: x[0].get_tag().get_category().get_name() == category,
                keywords
            )
        else:
            keywords_allowed = keywords

        return self._make_counts_from_flat(keywords_allowed)

    def _propogate_count(self, targets, count):
        return map(lambda x: (x, count), targets)

    def _make_counts_from_flat(self, obj_tuples):
        str_tuples = map(lambda x: (x[0].get_name(), x[1]), obj_tuples)
        
        ret_counts = {}
        for name, count in str_tuples:
            ret_counts[name] = ret_counts.get(name, 0) + count

        return self._convert_dict_to_counted_groups(ret_counts)

    def _convert_dict_to_counted_groups(self, target: typing.Dict[str, int]) -> COUNTED_GROUPS:
        return [CountedGroup(x[0], x[1]) for x in target.items()]

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
