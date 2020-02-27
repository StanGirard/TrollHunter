import requests
import xml.etree.ElementTree as ET
r = requests.get('https://www.washingtonpost.com/arcio/news-sitemap/')
print(r.content)
root = ET.fromstring(r.content)
for child in root.iter('*'):
    print(child.tag)