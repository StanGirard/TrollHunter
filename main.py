import requests
import xml.etree.ElementTree as ET
from news_crawler.sitemap.sitemap import parse_sitemap
from news_crawler.sitemap.extractor import extract_text_from_url
import pandas as pd
from news_crawler.sitemap.data_elastic import elastic_sitemap
from news_crawler.news_entry import news_crawler

#elastic_sitemap("https://www.lemonde.fr/sitemap_news.xml",["loc", "lastmod", "news:keywords"], sort = "loc", influxdb = True)
news_crawler()





