import sys
sys.path.append("../")
from TrollHunter.news_crawler.sitemap import parse_sitemap
import time
import pandas as pd

class SitemapInfo:
    def __init__(self, baseUrl, headers):
        self._headers = headers
        self._baseUrl = baseUrl
        self._pdResult = self._retriveUrlsByMap(self._baseUrl)
        if self._pdResult is not False:
            self._fetchAllUrlInfo()

    def _retriveUrlsByMap(self, map, baseUrl, headers):
        result = parse_sitemap(map, )
        # print(result)
        return result if result is not False else pd.DataFrame()

    def _fetchAllUrlInfo(self):
        for index, row in self._pdResult.iterrows():
            date = row[2].split(".")[0]
            timestamp = 0
            if date != "None":
                timestamp = time.mktime(time.strptime(date, '%Y-%m-%dT%H:%M:%S'))

            row[2] = timestamp

    def getResult(self) -> pd.DataFrame:
        return self._pdResult
