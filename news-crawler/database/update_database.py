import sqlite3
import sys
import importlib

sys.path.append("../")
deMod = importlib.import_module("data_elastic")

# connect to the local DB
conn = sqlite3.connect('./trollhunter.db')
print("Opened database successfully")

# select all providers
cursor = conn.execute("SELECT id, url_provider, site_map_path from NEWS_PROVIDERS")

headers = ["loc", "lastmod", "image:loc", "news:keywords", "news:title"]

for row in cursor:
    site_map_url = row[1]+row[2]
    deMod.elastic_sitemap(site_map_url, headers, sort = "lastmod")

print("Operation done successfully")
conn.close()