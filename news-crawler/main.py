import requests
import xml.etree.ElementTree as ET
from sitemap import parse_sitemap
from extractor import extract_text_from_url

print(parse_sitemap("https://primates.dev/sitemap.xml", ["loc", "lastmod"]))
#print(extract_text_from_url("https://primates.dev"))





