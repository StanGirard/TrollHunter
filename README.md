# TrollHunter

Added Python Package building

## Workflow

- [Github Flow](https://guides.github.com/introduction/flow/)
- Github Projects

## Cloud

- [Digital Ocean](https://m.do.co/c/f9dca2b1ecc8)

## Twint API


## News Indexer

The second main part of the project is the crawler and indexer of news.

For this, we use the sitemap xml file of news websites to crawl all the articles. In a sitemap file, we extract the tag
*sitemap* and *url*.

The *sitemap* tag is a link to a child sitemap xml file for a specific category of articles in the website.

The *url* tag represents an article/news of the website.  

The root url of a sitemap is stored in a postgres database with a trust level of the website (Oriented, Verified,
Fake News, ...) and headers. The headers are the tag we want to extract from the *url* tag which contains details about
the article (title, keywords, publication date, ...).

The headers are the list of fields use in the index pattern of ElasticSearch.
 
In crawling sitemaps, we insert the new child sitemap in the database with the last modification date or update it for
the ones already in the database. The last modification date is used to crawl only sitemaps which change since the
last crawling.

The data extracts from the *url* tags are built in a dataframe then sent in ElasticSearch for further utilisation with 
the request in Twint API.

In the same time, some sitemaps don't provide the keywords for their articles. Hence, from ElasticSearch we retrieve the
entries without keywords. Then, we download the content of the article and extract the keywords thanks to NLP. Finally,
we update the entries in ElasticSearch.

#### Run
For the crawler/indexer:

```python
from TrollHunter.news_crawler import scheduler_news

scheduler_news()
```

For updating keywords:
```python
from TrollHunter.news_crawler import scheduler_keywords

scheduler_keywords()
```

Or see with the [main](https://github.com/StanGirard/TrollHunter/tree/master/docker/news_crawler) use with docker.  

## TODO

- [ ] Make a better doc 
- [ ] Start the doc



