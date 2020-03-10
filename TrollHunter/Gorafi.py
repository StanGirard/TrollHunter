from TrollHunter.news_crawler.database import get_all_sitemap
from TrollHunter.news_crawler.sitemap import elastic_sitemap


class Gorafi:

    def __init__(self, headers=None, db_sitemap=None, sort=None):
        self.client_influxDB = None
        self.headers = ["loc", "lastmod", "news:keywords"]
        self.db_sitemap = {x[0]: x for x in get_all_sitemap()}
        self.sort = "loc"
        self.influxdb = True
        self.host = "142.93.170.234"
        self.port = 9200
        self.user = "elastic"
        self.password = "changeme"
        if headers:
            self.headers = headers
        if db_sitemap:
            self.db_sitemap = db_sitemap
        if sort:
            self.sort = sort

    def set_headers(self, headers):
        self.headers = headers
        
    def set_influx(self, activate):
        self.influxdb = activate

    def set_elastic(self, host, port, user, password):
        self.host = host
        self.port = port
        self.user = user
        self.password = password
    

    def sitemap(self, url):
        elastic_sitemap(url,self.headers, self.db_sitemap, host = self.host,
                        port = self.port, user = self.user, password = self.password,
                        sort = self.sort, influxdb = self.influxdb)
