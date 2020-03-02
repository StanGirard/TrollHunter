import requests
import xml.etree.ElementTree as ET
from sitemap import parse_sitemap
from extractor import extract_text_from_url
import pandas as pd

dataframe = parse_sitemap("https://www.washingtonpost.com/arcio/news-sitemap/", ["loc", "lastmod","news:title" ,"news:keywords"])
#print(extract_text_from_url("https://primates.dev"))
print(dataframe)
#dataframe.to_csv(r'./data.csv')





