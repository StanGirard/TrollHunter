import requests
import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup as Soup
import pandas as pd
import hashlib

# Pass the headers you want to retrieve from the xml such as ["loc", "lastmod"]
def parse_sitemap( url,headers):
    resp = requests.get(url)
    # we didn't get a valid response, bail
    if (200 != resp.status_code):
        return False

    # BeautifulSoup to parse the document
    soup = Soup(resp.content, "xml")

    # find all the <url> tags in the document
    urls = soup.findAll('url')
    sitemaps = soup.findAll('sitemap')
    new_list = ["Source"] + headers
    panda_out_total = pd.DataFrame([], columns=new_list)
    # no urls? bail
    if not urls and not sitemaps:
        return False
    if sitemaps:
        for u in sitemaps:
            test = u.find('loc').string
            panda_recursive = parse_sitemap(test, headers)
            panda_out_total = pd.concat([panda_out_total, panda_recursive], ignore_index=True)
            print("Sitemap: " + test )
            print(panda_out_total)
        return

    # storage for later...
    out = []

    # extract what we need from the url
    hash_sitemap = hashlib.md5(str(url).encode('utf-8')).hexdigest()
    for u in urls:
        values = [hash_sitemap]
        for head in headers:
            loc = None
            loc = u.find(head)
            if not loc:
                loc = "None"
            else:
                loc = loc.string
            values.append(loc)

        #prio = u.find('priority').string
        #change = u.find('changefreq').string
        
        out.append(values)
    
    
    panda_out = pd.DataFrame(out, columns= new_list)
    panda_out = pd.concat([panda_out, panda_out_total], ignore_index=True)
    return panda_out
