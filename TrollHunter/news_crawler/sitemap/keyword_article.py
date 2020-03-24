from elasticsearch import Elasticsearch
from newspaper import Article

from TrollHunter.loggers import InfluxDBLog


def get_null_keywords_es(es, size):
    result = es.search(index='sitemaps', q='-news\:keywords:*', _source_includes="news:keywords", size=size)
    return result['hits']['hits']


def if_influx_url(influxdb, url):
    if influxdb:
        InfluxDBLog().addEntry("Sitemap", "Keywords", 1, "URL", url)


def set_keywords(hit):
    article = Article(hit['_id'])
    article.download()
    article.parse()
    article.nlp()
    hit['_source']['news:keywords'] = ",".join(article.keywords)
    return hit


def update_keyword_es(es, hit):
    es.update(index='sitemaps',
              id=hit['_id'],
              body={"doc": {"news:keywords": hit['_source']['news:keywords']}})


def define_keywords_article(size=100, host="142.93.170.234", port=9200, user="elastic", password="changeme", influx_db=False):
    es = Elasticsearch(hosts=[{'host': host, 'port': port}], http_auth=(user, password))
    for hit in get_null_keywords_es(es, size):
        hit = set_keywords(hit)
        if_influx_url(influx_db, hit['_id'])
        update_keyword_es(es, hit)

