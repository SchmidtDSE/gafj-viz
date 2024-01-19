import csv
import io
import itertools
import typing

import article_getter


class StatGenerator:

    def __init__(self, inner_getter: article_getter.ArticleGetter):
        self._inner_getter = inner_getter

    def execute(self, params: typing.Dict) -> typing.Dict[str, float]:
        matching = self._inner_getter.execute_to_obj(params)
        dimension = params['dimension']

        strategy = {
            'country': lambda x: [x.get_country()],
            'keyword': lambda x: x.get_keywords(),
            'tag': lambda x: x.get_tags(),
            'category': lambda x: x.get_categories()
        }.get(dimension, None)

        if strategy is None:
            return []

        matching_values_nest = list(map(strategy, matching))
        matching_values = itertools.chain(*matching_values_nest)

        counts = {}
        total = len(matching_values_nest)
        for value in matching_values:
            counts[value] = counts.get(value, 0) + 1

        ret_tuples = map(lambda item: (item[0], item[1] / total), counts.items())
        return dict(ret_tuples)


def make_csv_str(target: typing.Dict[str, float]) -> str:
    output_target = io.StringIO()

    target_flat = map(lambda x: {'name': x[0], 'percent': x[1]}, target.items())

    writer = csv.DictWriter(output_target, fieldnames=['name', 'percent'])
    writer.writeheader()
    writer.writerows(target_flat)

    return output_target.getvalue()


def lambda_handler(event, context):
    inner_getter = article_getter.AwsLambdaArticleGetter()
    generator = StatGenerator(inner_getter)

    matching = generator.execute(event)
    csv_str = make_csv_str(matching)

    res = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv',
            'Content-Disposition': 'attachment',
            'filename': 'articles_summary.csv'
        },
        'body': csv_str
    }
    return res
