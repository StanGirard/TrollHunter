import sqlite3
import sys

sys.path.append("../")
from SitemapInfoGetter import SitemapInfo

# connect to the local DB
conn = sqlite3.connect('./trollhunter.db')
print("Opened database successfully")

# select all providers
cursor = conn.execute("SELECT id, url_provider, site_map_path from NEWS_PROVIDERS")

for row in cursor:
    site_map_url = row[1]+row[2]
    sitemapGetter = SitemapInfo(site_map_url)


print("Operation done successfully")
conn.close()
