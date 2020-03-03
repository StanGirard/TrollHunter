import sys
sys.path.append("../")
from sitemap import parse_sitemap
import time

class SitemapInfo:
    def __init__(self, baseUrl):
        self._baseUrl = baseUrl
        self._pdResult = self._retriveUrlsByMap(self._baseUrl)
        if self._pdResult is not False:
            self._fetchAllUrlInfo()

    def _retriveUrlsByMap(self, map):
        result = parse_sitemap(map, ["loc", "lastmod", "image:loc", "news:keywords", "news:title"])
        # for each urls, get info
        # print(result)
        return result

    def _fetchAllUrlInfo(self):
        for index, row in self._pdResult.iterrows():
            date = row[2].split(".")[0]
            timestamp = 0
            if date != "None":
                timestamp = time.mktime(time.strptime(date, '%Y-%m-%dT%H:%M:%S'))

            row[2] = timestamp

        # print(self._pdResult)
