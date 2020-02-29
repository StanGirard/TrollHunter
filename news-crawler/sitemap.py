import requests
import xml.etree.ElementTree as ET

class Sitemap:
    def __init__(self, url):
        self.url = url
        self.xmlDict = []
        
    def request_sitemap(self):
        raw_content = requests.get(self.url)
        self.root_xml = ET.fromstring(raw_content)
        return self.root_xml
