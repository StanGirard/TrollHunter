from TrollHunter.news_crawler.sitemap import elastic_sitemap
from TrollHunter.news_crawler.database import get_all_sitemap
from TrollHunter import Gorafi

db_sitemap = {x[0]: x for x in get_all_sitemap()}
hello = Gorafi()
hello.sitemap("https://www.lemonde.fr/sitemap_news.xml")
#elastic_sitemap("https://www.lemonde.fr/sitemap_news.xml",["loc", "lastmod", "news:keywords"], db_sitemap, sort = "loc", influxdb = True)






