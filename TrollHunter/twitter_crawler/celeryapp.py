from __future__ import absolute_import

import sys

from celery import Celery
from celery.bin import worker
app = Celery('crawler-api',
             broker='pyamqp://guest@142.93.170.234',
             include=['TrollHunter.twitter_crawler.twint_api.request_twint'])
app_crawler = Celery('crawler',
             broker='pyamqp://guest@142.93.170.234',
             include=['TrollHunter.twitter_crawler.crawler'])
def run_api_worker():
    worker_celery = worker.worker(app=app)
    option = {'loglevel': 'INFO'}
    worker_celery.run(**option)
    # app.start(["-A", "request", "worker", "--loglevel","info"])
def run_crawler():
    worker_celery = worker.worker(app=app_crawler)
    option = {'loglevel': 'INFO'}
    worker_celery.run(**option)

if __name__ == '__main__':
    arg = sys.argv[1:]
    if len(arg) == 0:
        run_crawler()
        run_api_worker()
    elif "api" in arg:
        run_api_worker()
    else :
        run_crawler()

