"""Alternative endpoint for generating query article statistics used for express version.

License: BSD
"""

import csv
import io
import itertools
import typing

import article_getter


class StatGenerator:
    """Utility to generate statistics outside the interactive visualization."""

    def __init__(self, inner_getter: article_getter.ArticleGetter):
        """Create a new generator.

        Args:
            inner_getter: Article getter to decorate with functionality to generate statistics.
        """
        self._inner_getter = inner_getter

    def execute(self, params: typing.Dict) -> typing.Dict[str, float]:
        """Execute a query and generate summary statistics to describe the resulting aggregation.

        Args:
            params: Dictionary with parameters describing the query.

        Returns:
            Mapping from group to count of matching articles in that group where group may be
            country, tag, category, keyword, etc.
        """
        matching = self._inner_getter.execute_to_obj(params)
        if 'queryStringParameters' in params:
            dimension = params['queryStringParameters']['dimension']
        else:
            dimension = params['dimension']

        strategy = {
            'country': lambda x: [x.get_country()],
            'keyword': lambda x: x.get_keywords(),
            'tag': lambda x: x.get_tags(),
            'category': lambda x: x.get_categories()
        }.get(dimension, None)

        if strategy is None:
            return {}

        matching_values_nest = list(map(strategy, matching))
        matching_values = itertools.chain(*matching_values_nest)

        counts: typing.Dict[str, float] = {}

        if dimension == 'country':
            country_counts = self.get_country_counts()
            total_getter = lambda x: country_counts[x]
        else:
            total = len(matching_values_nest)
            total_getter = lambda x: total

        for value in matching_values:
            counts[value] = counts.get(value, 0.0) + 1

        ret_tuples = map(lambda item: (item[0], item[1] / total_getter(item[0])), counts.items())
        return dict(ret_tuples)

    def get_country_counts(self) -> typing.Dict[str, int]:
        """Get the total number of articles per country in the dataset.

        Returns:
            Mapping from name of country to count of articles.
        """
        all_articles = self._inner_getter.execute_to_obj({'queryStringParameters': {}})
        all_article_countries = map(lambda x: x.get_country(), all_articles)

        ret_counts: typing.Dict[str, int] = {}
        for country in all_article_countries:
            ret_counts[country] = ret_counts.get(country, 0) + 1

        return ret_counts


def make_csv_str(target: typing.Dict[str, float]) -> str:
    """Convert a collection of group counts to the string contents of a CSV file.

    Args:
        target: The values to serialize to CSV.

    Returns:
        The input target as a CSV string.
    """
    output_target = io.StringIO()

    target_flat = map(lambda x: {'name': x[0], 'percent': x[1]}, target.items())

    writer = csv.DictWriter(output_target, fieldnames=['name', 'percent'])
    writer.writeheader()
    writer.writerows(target_flat)

    return output_target.getvalue()


def lambda_handler(event, context):
    """Entrypoint / driver for Lambda-based execution.

    Args:
        event: Information about the Lambda event including query parameters.
        context: Unused Lambda contextual information.

    Returns:
        Lambda compatible HTTP response.
    """
    inner_getter = article_getter.AwsLambdaArticleGetter()
    generator = StatGenerator(inner_getter)

    matching = generator.execute(event)
    csv_str = make_csv_str(matching)

    res = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment',
            'filename': 'articles_summary.csv',
            'Access-Control-Allow-Origin': '*'
        },
        'body': csv_str
    }
    return res
