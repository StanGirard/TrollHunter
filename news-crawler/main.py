import requests
import xml.etree.ElementTree as ET
r = requests.get('https://www.washingtonpost.com/arcio/news-sitemap/')
#print(r.content)
xmlDict = {}
root = ET.fromstring(r.content)
for child in root.iter('*'):
    print(child.tag)
for sitemap in root:
    children = sitemap.getchildren()
    xmlDict[children[0].text] = children[1].text
print (xmlDict)