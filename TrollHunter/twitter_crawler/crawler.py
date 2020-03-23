import getopt
import sys
import json

from TrollHunter.twitter_crawler.celeryapp import app
from TrollHunter.twitter_crawler.twint import twint
from TrollHunter.twitter_crawler.twint_api.elastic import Elastic
from TrollHunter.twitter_crawler.twint_api import request_twint

es = Elastic()
@app.task
def crawl(list_user,args):
    args_copy = args.copy()

    list_user = json.loads(list_user)
    if "depth" in args_copy.keys():
        args_copy["depth"] = int(args_copy["depth"]) - 1
    for user in list_user:
        if not es.is_crawled(user):
            request_twint.get_info_from_user.delay(user,args_copy)

    # elastic.is_crawled
    # list_tweet = crawl_tweet(args)

