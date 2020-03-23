from elasticsearch import Elasticsearch
from newspaper import Article


def get_null_keywords_es(es, size):
    result = es.search(index='sitemaps', q='-news\:keywords:*', _source_includes="news:keywords", size=size)
    return result['hits']['hits']


def set_keywords(hit):
    # call texto
    keyword = ''
    article = Article(hit['_id'])
    article.download()
    article.parse()
    article.nlp()
    print(article.keywords)
    hit['_source']['news:keywords'] = keyword
    return hit


def update_keyword_es(es, hit):
    es.update(index='sitemaps',
              id=hit['_id'],
              body={
                  "script": {
                      "source": "ctx._source.news:keywords = params.keywords",
                      "lang": "painless",
                      "params": {"keywords": hit['_source']['news:keywords']},
                  }
              })


def define_keywords_article(size=100, host = "142.93.170.234", port = 9200, user="elastic", password="changeme"):
    es = Elasticsearch(hosts=[{'host': host, 'port': port}], http_auth=(user, password))
    for hit in get_null_keywords_es(es, size):
        hit = set_keywords(hit)
        # update_keyword_es(es, hit)


define_keywords_article(1)
