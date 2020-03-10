from TrollHunter.Gorafi.sitemap.data_elastic import elastic_sitemap
from TrollHunter.Gorafi.database.postgres_database import get_all_sitemap

db_sitemap = {x[0]: x for x in get_all_sitemap()}

elastic_sitemap("https://www.lemonde.fr/sitemap_news.xml",["loc", "lastmod", "news:keywords"], db_sitemap, sort = "loc", influxdb = True)






