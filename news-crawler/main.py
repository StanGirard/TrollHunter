import requests
import xml.etree.ElementTree as ET
from sitemap import parse_sitemap


print(parse_sitemap("https://primates.dev/sitemap-posts.xml", ["loc", "lastmod"]))







