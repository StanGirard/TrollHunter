import pandas as pd
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers

# Check for empty values

from TrollHunter.news_crawler.sitemap.sitemap import parse_sitemap


def safe_value(field_val):
    return field_val if not pd.isna(field_val) else "Other"


def filterKeys(document, headers):
    use_these_keys = ["Source"] + headers + ['Trust level']
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


def elastic_sitemap(sitemap, trust_levels, db_sitemap, host = "142.93.170.234", port = 9200, user = "elastic", password = "changeme", sort = None, influxdb = False):
    es = Elasticsearch(hosts=[{'host': host, 'port': port}], http_auth=(user, password) )
    dataframe = parse_sitemap(sitemap, trust_levels, db_sitemap, es, indexEs = "sitemaps", sort = sort, influxdb = influxdb, range_check=20)
    print(dataframe)
    if type(dataframe) == bool:
        return

    transform_none_lastmod(dataframe)
    length_dataframe = len(dataframe.index)
    if length_dataframe > 0:
        print(length_dataframe, " doc(s) will be put in ES")
        print(helpers.bulk(es, doc_generator(dataframe, sitemap[2])))
    else:
        print("No new value")


def transform_none_lastmod(pdResult: pd.DataFrame):
    for index, row in pdResult.iterrows():
        date = row[2].split(".")[0]
        timestamp = 0
        if date != "None":
            date_in = date[:19]
            timestamp = time.mktime(time.strptime(date_in, '%Y-%m-%dT%H:%M:%S'))

        row[2] = timestamp


def iterator(ar):
    for item in ar:
        try:
            yield item
        except StopIteration:
            return
