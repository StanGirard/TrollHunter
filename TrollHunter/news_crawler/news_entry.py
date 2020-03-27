from TrollHunter.news_crawler.database import get_sitemap_parent, get_all_sitemap, get_trust_levels
from TrollHunter.news_crawler.sitemap import elastic_sitemap, define_keywords_article
import time


def news_crawler():
    db_sitemap = {x[0]: x for x in get_all_sitemap()}
    trust_levels = {x[0]: x[1] for x in get_trust_levels()}
    for parent in get_sitemap_parent():
        elastic_sitemap(parent, trust_levels, db_sitemap, sort='loc', influxdb=True)


def scheduler_news(time_interval):
    """
    Entry point for crawling sitemaps and indexing news in ElasticSearch.
    Every time_interval minutes, sitemaps are crawled to index the new articles.

    :param time_interval: frequency in minutes for crawling sitemaps
    """
    print('Start crawler/indexer sitemap')
    while True:
        start = time.time()
        try:
            news_crawler()
        except Exception as error:
            print(error)
        print('Crawler Sleeping')
        sleep = time.time() - start
        if sleep < time_interval:
            time.sleep(time_interval - sleep)


def scheduler_keywords(time_interval, max_entry):
    """
    Entry point for extracting and updating in ElasticSearch the news entries without keywords.
    Every time_interval in minutes, maximum max_entry news entries are updated.

    :param time_interval: frequency in minutes for updating keywords
    :param max_entry: maximum number of news retrieve for ElasticSearch
    """
    print('Start extract keywords')
    while True:
        start = time.time()
        try:
            define_keywords_article(max_entry, influx_db=True)
        except Exception as error:
            print(error)
        print('Extract Keywords Sleep')
        sleep = time.time() - start
        if sleep < time_interval:
            time.sleep(time_interval - sleep)
