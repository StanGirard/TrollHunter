import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from sitemap import parse_sitemap
import requests

#Check for empty values
def safe_value(field_val):
    return field_val if not pd.isna(field_val) else "Other"

use_these_keys = ["Source","loc", "lastmod"]
def filterKeys(document):
    return {key: document[key] for key in use_these_keys }

def doc_generator(df):
    df_iter = df.iterrows()
    for index, document in df_iter:
        try:
            yield {
                "_index": 'sitemaps',
                "_type": "_doc",
                "_id" : f"{document['loc']}",
                "_source": filterKeys(document),
            }
        except StopIteration:
            return
        
   


dataframe = parse_sitemap("https://primates.dev/sitemap.xml", ["loc", "lastmod"])


url = "142.93.170.234"

es = Elasticsearch(hosts = [{'host': url, 'port': 9200}],http_auth=('elastic', 'changeme'),)
helpers.bulk(es, doc_generator(dataframe))


