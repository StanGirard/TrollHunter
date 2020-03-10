from news_crawler.database.postgres_database import get_sitemap_parent, get_all_sitemap
from news_crawler.sitemap.data_elastic import elastic_sitemap


def news_crawler():
    db_sitemap = {x[0]: x for x in get_all_sitemap()}
    for parent in get_sitemap_parent():
        elastic_sitemap(parent[0], parent[2], db_sitemap, sort='loc', influxdb=True)
