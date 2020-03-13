from TrollHunter.news_crawler.database import get_sitemap_parent, get_all_sitemap, get_trust_levels
from TrollHunter.news_crawler.sitemap import elastic_sitemap
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
        print('Sleeping')
        sleep = time.time() - start
        if sleep < 7200:
            time.sleep(7200 - sleep)
