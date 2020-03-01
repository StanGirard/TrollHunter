import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as Soup
import pandas as pd

# Pass the headers you want to retrieve from the xml such as ["loc", "lastmod"]
def parse_sitemap( url,headers):
    resp = requests.get(url)
    # we didn't get a valid response, bail
    if (200 != resp.status_code):
        return False

    # BeautifulSoup to parse the document
    soup = Soup(resp.content)

    # find all the <url> tags in the document
    urls = soup.findAll('url')

    # no urls? bail
    if not urls:
        return False

    # storage for later...
    out = []

    # extract what we need from the url
    for u in urls:
        values = []
        for head in headers:
            loc = u.find(head).string
            values.append(loc)

        #prio = u.find('priority').string
        #change = u.find('changefreq').string
        
        out.append(values)
    panda_out = pd.DataFrame(out, columns= headers)
    return panda_out
