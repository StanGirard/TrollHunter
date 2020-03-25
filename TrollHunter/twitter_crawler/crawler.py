import getopt
import signal
import sys
import json
import time
from datetime import date
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


def crawl_from_search (args):
    signal.signal(signal.SIGINT, exit_)
    signal.signal(signal.SIGTERM, exit_)
    now = date.today()

    print('Start crawler twitter')
    while True:
        start = time.time()
        try:
            request_twint.get_tweet_from_search.delay(args)
            args["since"] = now.isoformat()
            now = date.today()
        except Exception as error:
            print(error)
        print('Sleeping')
        sleep = time.time() - start
        if sleep < 7200:
            time.sleep(7200 - sleep)

def exit_():
    sys.exit()


if __name__ == '__main__':
    args = {}
    args["search"] = "(#Covid-19)"
    args["limit"] = 100
    args["follow_limit"] = 10
    args["tweet_interact"] = 1
    args["tweet"] = 0
    crawl_from_search(args)
