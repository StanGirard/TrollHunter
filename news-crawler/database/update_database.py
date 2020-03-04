import sqlite3
import sys
import importlib
from elasticsearch import Elasticsearch
from elasticsearch import helpers

sys.path.append("../")
from SitemapInfoGetter import SitemapInfo
deMod = importlib.import_module("data_elastic")

# connect to the local DB
conn = sqlite3.connect('./trollhunter.db')
print("Opened database successfully")

# select all providers
cursor = conn.execute("SELECT id, url_provider, site_map_path from NEWS_PROVIDERS")

getter = []

url = "142.93.170.234"

es = Elasticsearch(hosts = [{'host': url, 'port': 9200}],http_auth=('elastic', 'changeme'),)

for row in cursor:
    site_map_url = row[1]+row[2]
    # get urls info from a specific provider
    res = SitemapInfo(site_map_url).getResult()
    if res.empty:
        print('Cannot update info from ' + site_map_url)
        continue

    kept = []
    for dic in deMod.doc_generator(res):
        if not deMod.check_id_in_es(es, dic["_index"], dic["_id"]):
            kept.append(dic)
        else:
            print("Already")

    if len(kept) > 0:
        helpers.bulk(es, deMod.iterator(kept))

print("Operation done successfully")
conn.close()
