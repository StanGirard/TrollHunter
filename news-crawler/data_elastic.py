import numpy as np
import pandas as pd
from elasticsearch import Elasticsearch
from elasticsearch import helpers
from sitemap import parse_sitemap
import requests

#Check for empty values
def safe_value(field_val):
    return field_val if not pd.isna(field_val) else "Other"

def filterKeys(document, headers):
    use_these_keys = ["Source"] + headers
    return {key: document[key] for key in use_these_keys }

def doc_generator(df, headers):
    df_iter = df.iterrows()
    for index, document in df_iter:
        try:
            yield {
                "_index": 'sitemaps',
                "_type": "_doc",
                "_id" : f"{document['loc']}",
                "_source": filterKeys(document, headers),
            }
        except StopIteration:
            return
        
def elastic_sitemap(url, headers, host = "142.93.170.234", port = 9200, user = "elastic", password = "changeme"):
    dataframe = parse_sitemap(url, headers)
    print(dataframe)
    es = Elasticsearch(hosts = [{'host': host, 'port': port}],http_auth=(user, password),)
    print(helpers.bulk(es, doc_generator(dataframe, headers)))

# to check if an id (here the url) already exists in the ES
def check_id_in_es(es: Elasticsearch, index: str, id: str):
    return es.exists(index, id)


