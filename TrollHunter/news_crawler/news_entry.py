from TrollHunter.news_crawler.database.postgres_database import get_sitemap_parent, get_all_sitemap, get_trust_levels
from TrollHunter.news_crawler.sitemap.data_elastic import elastic_sitemap
import time


def news_crawler():
    db_sitemap = {x[0]: x for x in get_all_sitemap()}
    trust_levels = {x[0]: x for x in get_trust_levels()}
    for parent in get_sitemap_parent():
        elastic_sitemap(parent, trust_levels, db_sitemap, sort='loc', influxdb=True)


def scheduler_news():
    start = time.time()
    while True:
        try:
            news_crawler()
        except Exception as error:
            print(error)
        sleep = time.time() - start
        if sleep < 7200:
            time.sleep(7200 - sleep)
