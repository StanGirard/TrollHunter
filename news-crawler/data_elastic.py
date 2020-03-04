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

    kept = []
    for dic in doc_generator(dataframe, headers):
        if not check_id_in_es(es, dic["_index"], dic["_id"]):
            kept.append(dic)
        else:
            print("Already " + dic["_id"])

    if len(kept) > 0:
        print(len(kept), " doc(s) will be put in ES")
        print(helpers.bulk(es, iterator(kept)))

def iterator(ar):
    for item in ar:
        try:
            yield item
        except StopIteration:
            return

# to check if an id (here the url) already exists in the ES
def check_id_in_es(es: Elasticsearch, index: str, id: str):
    return es.exists(index, id)


