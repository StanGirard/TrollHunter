from __future__ import absolute_import
import os
import sys

from celery import Celery
from celery.bin import worker
app = Celery('crawler-api',
             broker='pyamqp://guest@' + os.environ["RABBITMQ_HOST"],
             include=['TrollHunter.twitter_crawler.twint_api.request_twint','TrollHunter.twitter_crawler.crawler'])

#Start worker rabbitmq

def run_crawler():
    worker_celery = worker.worker(app=app)
    option = {'loglevel': 'INFO'}
    worker_celery.run(**option)

if __name__ == '__main__':
    run_crawler()

