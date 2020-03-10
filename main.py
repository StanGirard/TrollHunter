from TrollHunter.Gorafi.sitemap.data_elastic import elastic_sitemap



elastic_sitemap("https://www.lemonde.fr/sitemap_news.xml",["loc", "lastmod", "news:keywords"], sort = "loc", influxdb = True)






