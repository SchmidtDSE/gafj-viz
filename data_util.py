import os
import sqlite3
import typing

OPT_STR = typing.Optional[str]
PATH_DB = 'articles.db'


class Query:

    def __init__(self, category: str, pre_category: OPT_STR, country: OPT_STR, tag: OPT_STR,
        keyword: OPT_STR):
        self._category = category
        self._pre_category = pre_category
        self._country = country
        self._tag = tag
        self._keyword = keyword

    def get_category(self) -> str:
        return self._category

    def has_pre_category(self) -> bool:
        return self._pre_category is not None 

    def get_pre_category(self) -> OPT_STR:
        return self._category

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


class CountedGroup:

    def __init__(self, name: str, count: int):
        self._name = name
        self._count = count

    def get_name(self) -> str:
        return self._name

    def get_count(self) -> int:
        return self._count


COUNTED_GROUPS = typing.List[CountedGroup]


class Result:

    def __init__(self, total_count: int, group_count: int, categories: COUNTED_GROUPS,
        countries: COUNTED_GROUPS, country_totals: COUNTED_GROUPS, tags: COUNTED_GROUPS,
        keywords: COUNTED_GROUPS):
        self._total_count = total_count
        self._group_count = group_count
        self._categories = categories
        self._countries = countries
        self._country_totals = country_totals
        self._tags = tags
        self._keywords = keywords

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


class DataAccessor:

    def execute_query(query: Query) -> Result:
        raise RuntimeError('Use implementor.')


class LocalDataAccessor(DataAccessor):

    def execute_query(self, query: Query) -> Result:
        connection = sqlite3.connect(PATH_DB)

        total_count = self._get_total_no_query(connection)

        group_count_raw = self._execute_sql(connection, query, 'total.sql', True)
        group_count = int(group_count_raw[0][0])

        def execute_inner(filename: str, include_category: bool) -> COUNTED_GROUPS:
            return self._execute_sql_for_counted_groups(
                connection,
                query,
                filename,
                include_category
            )

        categories = execute_inner('categories.sql', True)
        countries = execute_inner('countries.sql', True)
        country_totals = execute_inner('countries.sql', False)
        tags = execute_inner('tags.sql', True)
        keywords = execute_inner('keywords.sql', True)

        connection.close()

        return Result(
            total_count,
            group_count,
            categories,
            countries,
            country_totals,
            tags,
            keywords
        )

    def _create_where_clause(self, query: Query, include_category: bool) -> str:
        clauses = []

        if include_category:
            clauses.append('category = ?')

        if query.has_country():
            clauses.append('country = ?')

        if query.has_tag():
            clauses.append('(token = ? AND tokenType = \'tag\')')

        if query.has_keyword():
            clauses.append('(token = ? AND tokenType = \'keyword\')')

        if len(clauses) == 0:
            clauses.append('1 = 1')

        return ' AND '.join(clauses)


    def _convert_query_to_params(self, sql_base: str, query: Query,
        include_category: bool) -> typing.List:

        def get_clauses() -> typing.List:
            clauses = []

            if include_category:
                clauses.append(query.get_category())

            if query.has_country():
                clauses.append(query.get_country())

            if query.has_tag():
                clauses.append(query.get_tag())

            if query.has_keyword():
                clauses.append(query.get_keyword())

            return clauses

        return get_clauses() * sql_base.count('WHERE_CLAUSE')

    def _execute_sql(self, connection: sqlite3.Connection, query: Query,
        filename: str, include_category: bool) -> typing.List[typing.Tuple]:
        cursor = connection.cursor()

        base_path = os.path.dirname(os.path.abspath(__file__))
        full_path = os.path.join(base_path, 'sql', filename)
        with open(full_path) as f:
            sql_base = f.read()

        sql = sql_base.replace(
            'WHERE_CLAUSE',
            'WHERE ' + self._create_where_clause(query, include_category)
        )

        result = cursor.execute(
            sql,
            self._convert_query_to_params(sql_base, query, include_category)
        )
        result_realized = list(result.fetchall())

        cursor.close()
        return result_realized


    def _execute_sql_for_counted_groups(self, connection: sqlite3.Connection, query: Query,
        filename: str, include_category: bool) -> COUNTED_GROUPS:
        
        def parse_counted_group(target: typing.Tuple) -> CountedGroup:
            return CountedGroup(target[0], int(target[1]))

        results_raw = self._execute_sql(connection, query, filename, include_category)
        return [parse_counted_group(x) for x in results_raw]

    def _get_total_no_query(self, connection: sqlite3.Connection) -> int:
        cursor = connection.cursor()
        cursor.execute('SELECT count(DISTINCT url) FROM output_frame')
        total_count = int(cursor.fetchall()[0][0])
        cursor.close()

        return total_count
