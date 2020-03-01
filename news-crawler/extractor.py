from inscriptis import get_text
import requests

def extract_text_from_url(url):
    text = ""
    try:
        html = requests.get(url).text
        #html = urllib.request.urlopen(i, timeout=3).read().decode("utf8")
        text = get_text(html)
        
    except:
        print("Error: " + url)
    return text