from TrollHunter.news_crawler.database import get_sitemap_parent, get_all_sitemap, get_trust_levels
from TrollHunter.news_crawler.sitemap import elastic_sitemap, define_keywords_article
import time


def news_crawler():
    db_sitemap = {x[0]: x for x in get_all_sitemap()}
    trust_levels = {x[0]: x[1] for x in get_trust_levels()}
    for parent in get_sitemap_parent():
        elastic_sitemap(parent, trust_levels, db_sitemap, sort='loc', influxdb=True)


def scheduler_news():
    print('Start crawler/indexer sitemap')
    while True:
        start = time.time()
        try:
            news_crawler()
        except Exception as error:
            print(error)
        print('Crawler Sleeping')
        sleep = time.time() - start
        if sleep < 7200:
            time.sleep(7200 - sleep)


def scheduler_keywords():
    print('Start extract keywords')
    while True:
        start = time.time()
        try:
            define_keywords_article(100, influx_db=True)
        except Exception as error:
            print(error)
        print('Extract Keywords Sleep')
        sleep = time.time() - start
        if sleep < 3600:
            time.sleep(3600 - sleep)
