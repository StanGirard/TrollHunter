import requests
from bs4 import BeautifulSoup as Soup
import pandas as pd
import hashlib
from database.postgres_database import insert_sitemap, update_sitemap, get_sitemap
from InfluxLog import InfluxDBLog
from elasticsearch import Elasticsearch

# to check if an id (here the url) already exists in the ES
def check_id_in_es(es: Elasticsearch, index: str, id: str):
    return es.exists(index, id)

def if_influx_url(influxdb, url):
    if influxdb:
        InfluxDBLog().addEntry("Sitemap", "Crawling", 1, "URL", url )

def sort_loc(x):
    res = x.find("loc")
    return res.string if res else "None"

# Pass the headers you want to retrieve from the xml such as ["loc", "lastmod"]
def parse_sitemap( url,headers, es: Elasticsearch, indexEs = "sitemaps", sort = None,  influxdb = False):
    resp = requests.get(url)

    # we didn't get a valid response, bail
    if (200 != resp.status_code):
        return False

    # BeautifulSoup to parse the document
    soup = Soup(resp.content, "xml")
    # find all the <url> tags in the document
    urls = soup.findAll('url')
    #Sorts the urls by the key specified
    if sort and urls:
        urls.sort(key=sort_loc)
    sitemaps = soup.findAll('sitemap')
    new_list = ["Source"] + headers
    panda_out_total = pd.DataFrame([], columns=new_list)


    if not urls and not sitemaps:
        return False

    # Recursive call to the the function if sitemap contains sitemaps
    if sitemaps:
        for u in sitemaps:
            if check_sitemap(u):
                test = u.find('loc').string
                panda_recursive = parse_sitemap(test, headers, es, sort, influxdb = influxdb)
                panda_out_total = pd.concat([panda_out_total, panda_recursive], ignore_index=True)

    # storage for later...
    out = []

    # Creates a hash of the parent sitemap
    hash_sitemap = hashlib.md5(str(url).encode('utf-8')).hexdigest()

    # Extract the keys we want
    count = 0
    for u in urls:
        if count % 10 == 0:
            if not check_id_in_es(es, indexEs, u.find("loc").string):
                count = 0
        values = [hash_sitemap]
        #Log into influxdb
        if_influx_url(influxdb, url)
        for head in headers:
            loc = None
            loc = u.find(head)
            if not loc:
                loc = "None"
            else:
                loc = loc.string
            values.append(loc)
        out.append(values)
        count += 1
        if count == 20:
            return build_panda_out(out, panda_out_total, new_list)

    return build_panda_out(out, panda_out_total, new_list)

def build_panda_out(out, panda_out_total, new_list):
    # Create a dataframe
    panda_out = pd.DataFrame(out, columns=new_list)

    # If recursive then merge recursive dataframe
    if not panda_out_total.empty:
        panda_out = pd.concat([panda_out, panda_out_total], ignore_index=True)

    # returns the dataframe
    return panda_out

def check_sitemap(sitemap):
    loc = sitemap.find('loc').string
    lastmod = sitemap.find('lastmod').string
    data_sitemap = get_sitemap(loc)
    if data_sitemap:
        if lastmod and data_sitemap[1]:
            if data_sitemap[1] != lastmod:
                update_sitemap(loc, lastmod)
            else:
                return False
    else:
        insert_sitemap(loc, lastmod)
    return True

