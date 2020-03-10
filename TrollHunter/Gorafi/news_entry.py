from news_crawler.database.postgres_database import get_sitemap_parent, get_all_sitemap
from news_crawler.sitemap.data_elastic import elastic_sitemap
import time


def news_crawler():
    db_sitemap = {x[0]: x for x in get_all_sitemap()}
    for parent in get_sitemap_parent():
        elastic_sitemap(parent[0], parent[2], db_sitemap, sort='loc', influxdb=True)


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


if __name__ == "__main__":
    scheduler_news()
