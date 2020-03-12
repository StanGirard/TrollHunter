import getopt
import sys

from TrollHunter.twitter_crawler.celeryapp import app_crawler
from TrollHunter.twitter_crawler.twint import twint
# from TrollHunter.twitter_crawler.twint_api.request_twint import  crawl_tweet

@app_crawler.task
def crawl(list_user,args):
    # list_tweet = crawl_tweet(args)
    print(args)

