import csv
import io

import smart_open

COLS = (
    'url',
    'titleOriginal',
    'titleEnglish',
    'published',
    'country',
    'keywordList',
    'tagList',
    'categoryList'
)
OBJ_PATH = 's3://gafj-topic-explorer/articles.csv'


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

    def to_dict(self) -> typing.Dict[str,str]:
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


def parse_row(target_str: str) -> typing.Dict:
    pieces = target_str.split('\t')
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


def execute_query(query_params: typing.Dict[str, str]) -> typing.Iterable[Article]:
    input_lines = smart_open.smart_open(OBJ_PATH, 'r')
    articles = map(parse_row, input_lines)

    if 'keyword' in query_params:
        target_keyword = query_params['keyword']
        articles = filter(lambda x: target_keyword in x.get_keywords(), articles)

    if 'tag' in query_params:
        target_tag = query_params['tag']
        articles = filter(lambda x: target_tag in x.get_tags(), articles)

    if 'category' in query_params:
        target_tag = query_params['category']
        articles = filter(lambda x: target_tag in x.get_categories(), articles)

    if 'country' in query_params:
        target_country = query_params['country']
        articles = filter(lambda x: x.get_country() == target_country, articles)

    articles = filter(lambda x: x.get_url() != 'url', articles)

    return articles


def make_csv_str(articles: typing.Iterable[Article]) -> str:
    articles_dicts = map(lambda x: x.to_dict(), articles)

    output_target = io.StringIO()
    
    writer = csv.DictWriter(output_target, fieldnames=COLS)
    writer.writeheader()
    writer.writerows(articles_dicts)

    return output_target.getvalue()


def request_handler(event, context):
    query_params = event['queryStringParameters']
    matching = execute_query(query_params)
    csv_str = make_csv_str(matching)

    res = {
        'statusCode': 200,
        'headers': {
            'Content-Type': 'text/csv'
        },
        'body': csv_str
    }
    return res
