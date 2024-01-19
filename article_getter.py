import codecs
import csv
import io
import os
import typing

boto_available = False
try:
    import boto3  # type: ignore
    boto_available = True
except:
    boto_available = False

COLS = (
    'url',
    'titleOriginal',
    'titleEnglish',
    'published',
    'country'
)
OBJ_BUCKET = 'gafj-topic-explorer'
OBJ_PATH = 'articles.csv'


class Article:

    def __init__(self, url: str, title_original: str, title_english: str, published: str,
        country: str, keywords: typing.List[str], tags: typing.List[str],
        categories: typing.List[str]):
        self._url = url
        self._title_original = title_original
        self._title_english = title_english
        self._published = published
        self._country = country
        self._keywords = keywords
        self._tags = tags
        self._categories = categories

    def get_url(self) -> str:
        return self._url

    def get_title_original(self) -> str:
        return self._title_original

    def get_title_english(self) -> str:
        return self._title_english

    def get_published(self) -> str:
        return self._published

    def get_country(self) -> str:
        return self._country

    def get_keywords(self) -> typing.List[str]:
        return self._keywords

    def get_tags(self) -> typing.List[str]:
        return self._tags

    def get_categories(self) -> typing.List[str]:
        return self._categories

    def to_dict(self) -> typing.Dict[str, str]:
        return {
            'url': self.get_url(),
            'titleOriginal': self.get_title_original(),
            'titleEnglish': self.get_title_english(),
            'published': self.get_published(),
            'country': self.get_country(),
            'keywordList': ';'.join(self.get_keywords()),
            'tagList': ';'.join(self.get_tags()),
            'categoryList': ';'.join(self.get_categories())
        }


class ArticleGetter:

    def execute_to_obj(self, params: typing.Dict) -> typing.Iterable[Article]:
        query_params = self._get_query_params(params)
        input_lines = self._get_source()
        matching = self._execute_query(query_params, input_lines)
        return matching

    def execute_to_native(self, params: typing.Dict):
        return self._make_response(self.execute_to_obj(params))

    def _parse_row(self, target_str: str) -> typing.Optional[Article]:
        pieces = target_str.split('\t')
        if len(pieces) != 8:
            return None

        return Article(
            pieces[0],
            pieces[1],
            pieces[2],
            pieces[3],
            pieces[4],
            pieces[5].split(';'),
            pieces[6].split(';'),
            pieces[7].split(';')
        )

    def _execute_query(self, query_params: typing.Dict[str, str],
        input_lines: typing.Iterable[str]) -> typing.Iterable[Article]:
        articles_with_none = map(lambda x: self._parse_row(x), input_lines)
        articles = filter(lambda x: x is not None, articles_with_none)  # type: ignore

        if 'keyword' in query_params:
            target_keyword = query_params['keyword']
            articles = filter(
                lambda x: target_keyword in x.get_keywords(),  # type: ignore
                articles
            )

        if 'tag' in query_params:
            target_tag = query_params['tag']
            articles = filter(lambda x: target_tag in x.get_tags(), articles)  # type: ignore

        if 'category' in query_params:
            target_category = query_params['category']
            articles = filter(
                lambda x: target_category in x.get_categories(),  # type: ignore
                articles
            )

        if 'country' in query_params:
            target_country = query_params['country']
            articles = filter(
                lambda x: x.get_country() == target_country,  # type: ignore
                articles
            )

        articles = filter(lambda x: x.get_url() != 'url', articles)  # type: ignore

        return articles  # type: ignore

    def _get_query_params(self, target: typing.Dict) -> typing.Dict:
        raise RuntimeError('Use implementor.')

    def _get_source(self) -> typing.Iterable[str]:
        raise RuntimeError('Use implementor.')

    def _make_response(self, matching: typing.Iterable[Article]) -> typing.Dict:
        raise RuntimeError('Use implementor.')


class AwsLambdaArticleGetter(ArticleGetter):

    def _get_query_params(self, target: typing.Dict) -> typing.Dict:
        return target['queryStringParameters']

    def _get_source(self) -> typing.Iterable[str]:
        if not boto_available:
            raise RuntimeError('Please install boto before lambda handler use.')

        client = boto3.client('s3')
        obj = client.get_object(Bucket=OBJ_BUCKET, Key=OBJ_PATH)
        body = obj['Body']
        stream_reader = codecs.getreader('utf-8')
        return stream_reader(body)

    def _make_response(self, matching: typing.Iterable[Article]):
        csv_str = self._make_csv_str(matching)

        res = {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'text/csv',
                'Content-Disposition': 'attachment',
                'filename': 'articles_export.csv',
                'Access-Control-Allow-Origin': '*'
            },
            'body': csv_str
        }
        return res

    def _make_csv_str(self, articles: typing.Iterable[Article]) -> str:
        articles_dicts = map(lambda x: x.to_dict(), articles)

        output_target = io.StringIO()

        writer = csv.DictWriter(output_target, fieldnames=COLS, extrasaction='ignore')
        writer.writeheader()
        writer.writerows(articles_dicts)

        return output_target.getvalue()


class LocalArticleGetter(ArticleGetter):

    def _get_query_params(self, target: typing.Dict) -> typing.Dict:
        return target

    def _get_source(self) -> typing.Iterable[str]:
        with open(os.path.join('csv', 'articles.csv')) as f:
            lines = f.readlines()

        return lines

    def _make_response(self, matching: typing.Iterable[Article]):
        return list(matching)


def lambda_handler(event, context):
    article_getter = AwsLambdaArticleGetter()
    return article_getter.execute_to_native(event)


def local_handler(params: typing.Dict) -> typing.List[Article]:
    article_getter = LocalArticleGetter()
    return article_getter.execute_to_native(params)  # type: ignore
