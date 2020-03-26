import pandas as pd
import time
from elasticsearch import Elasticsearch
from elasticsearch import helpers
import os
from dotenv import load_dotenv
load_dotenv()

# Check for empty values

from TrollHunter.news_crawler.sitemap.sitemap import parse_sitemap


def safe_value(field_val):
    return field_val if not pd.isna(field_val) else "Other"


def filterKeys(document, headers):
    """
    Filter a dictionary to match an index pattern in ElasticSearch

    :param document: dictionary to filter
    :param headers: fields in the pattern
    :return: dictionary only with the pattern's fields
    """
    use_these_keys = ["Source"] + headers + ['Trust level']
    return {key: document[key] for key in use_these_keys }


def doc_generator(df, headers):
    """
    Convert a dataframe to an ElasticSearch format.

    :param df: dataframe to convert
    :param headers: labels of the pattern's fields in ElasticSearch
    """
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


def elastic_sitemap(sitemap, trust_levels, db_sitemap, host = str(os.getenv("ELASTIC_SERVER")), port = os.getenv("ELASTIC_PORT"), user = os.getenv("ELASTIC_USER"), password = os.getenv("ELASTIC_PASSWORD"), sort = None, influxdb = False):
    """
    Parse a sitemap tree and aggregate the news in a dataframe.
    Then insert them in an index pattern in ElasticSearch.

    :param sitemap: the sitemap root to parse
    :param trust_levels: map to get the label of a trust levels with its id
    :param db_sitemap: map to get the sitemap's details with is url
    :param host: ElasticSearch host
    :param port: ElasticSearch port
    :param user: ElasticSearch user
    :param password: ElasticSearch password
    :param sort: column to sort the urls
    :param influxdb: true to emit event, false otherwise
    """
    
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
    """
    Transform the date in a dataframe to be the same for different sources and compliant with ElasticSearch.

    :param pdResult: dataframe with the date to transform
    """
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
