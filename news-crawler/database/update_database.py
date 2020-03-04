import sqlite3
import sys
from elasticsearch import Elasticsearch

sys.path.append("../")
from SitemapInfoGetter import SitemapInfo

# connect to the local DB
conn = sqlite3.connect('./trollhunter.db')
print("Opened database successfully")

# select all providers
cursor = conn.execute("SELECT id, url_provider, site_map_path from NEWS_PROVIDERS")

getter = []
for row in cursor:
    site_map_url = row[1]+row[2]
    # get urls info from a specific provider
    res = SitemapInfo(site_map_url).getResult()
    if not res:
        print('Cannot update info from ' + site_map_url)
        continue


print("Operation done successfully")
conn.close()
