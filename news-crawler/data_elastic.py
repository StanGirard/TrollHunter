import numpy as np
import pandas as pd
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

from sitemap import parse_sitemap, check_id_in_es
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

def elastic_sitemap(url, headers, host = "142.93.170.234", port = 9200, user = "elastic", password = "changeme", sort = None, influxdb = False):
    es = Elasticsearch(hosts=[{'host': host, 'port': port}], http_auth=(user, password), )

    dataframe = parse_sitemap(url, headers, es, indexEs = "sitemaps", sort = sort, influxdb = influxdb)

    print(dataframe)
    if type(dataframe) == bool:
        return

    transform_none_lastmod(dataframe)

    kept = []
    count = 1
    for dic in doc_generator(dataframe, headers):
        if not check_id_in_es(es, dic["_index"], dic["_id"]):
            kept.append(dic)
        else:
            print("Already " + dic["_id"], count)
        count += 1

    if len(kept) > 0:
        print(len(kept), " doc(s) will be put in ES")
        print(helpers.bulk(es, iterator(kept)))

def transform_none_lastmod(pdResult: pd.DataFrame):
    for index, row in pdResult.iterrows():
        date = row[2].split(".")[0]
        timestamp = 0
        if date != "None":
            timestamp = time.mktime(time.strptime(date, '%Y-%m-%dT%H:%M:%S'))

        row[2] = timestamp

def iterator(ar):
    for item in ar:
        try:
            yield item
        except StopIteration:
            return
