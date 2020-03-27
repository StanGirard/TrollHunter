from elasticsearch import Elasticsearch
from newspaper import Article
import os
from dotenv import load_dotenv
load_dotenv()
from TrollHunter.loggers import InfluxDBLog


def get_null_keywords_es(es, size):
    """
    Get from ElasticSearch the news entries which don't contain keywords.

    :param es: ElasticSearch connection
    :param size: limit of news which are retrieved
    :return: list of news without keywords
    """
    result = es.search(index='sitemaps', q='-news\:keywords:*', _source_includes="news:keywords", size=size)
    return result['hits']['hits']


def if_influx_url(influxdb, url):
    """
    Emit event in InfluxDb for monitoring, if set.
    Monitoring event: Update Keyword in ES

    :param influxdb: true for monitoring, false otherwise
    :param url: news'url linked to the event
    """
    if influxdb:
        InfluxDBLog().addEntry("Sitemap", "Keywords", 1, "URL", url)


def set_keywords(hit):
    """
    Get the content of the news from an url and extract the keywords with NLP.

    :param hit: news entry which contains the url of the news
    :return: the news entry with keywords
    """
    article = Article(hit['_id'])
    article.download()
    article.parse()
    article.nlp()
    hit['_source']['news:keywords'] = ",".join(article.keywords)
    return hit


def update_keyword_es(es, hit):
    """
    Update keywords of a news entry in ElasticSearch

    :param es: ElasticSearch connection
    :param hit: news entry to update
    """
    es.update(index='sitemaps',
              id=hit['_id'],
              body={"doc": {"news:keywords": hit['_source']['news:keywords']}})


def define_keywords_article(size=100, host=os.getenv("ELASTIC_SERVER"), port=os.getenv("ELASTIC_PORT"), user=os.getenv("ELASTIC_USER"), password=os.getenv("ELASTIC_PASSWORD"), influx_db=False):
    """
    Get news entries from ElasticSearch without keywords.
    For each entry extracts keywords and updates the value in ElasticSearch.
    If influx_db is set, emits an event for each entry

    :param size: max number of entries for updating
    :param host: ElasticSearch host
    :param port: ElasticSearch port
    :param user: ElasticSearch user
    :param password: ElasticSearch password
    :param influx_db: true to emit event, false otherwise
    """
    es = Elasticsearch(hosts=[{'host': host, 'port': port}], http_auth=(user, password))
    for hit in get_null_keywords_es(es, size):
        try:
            hit = set_keywords(hit)
        except Exception as error:
            print(error)
            continue
        if_influx_url(influx_db, hit['_id'])
        update_keyword_es(es, hit)

