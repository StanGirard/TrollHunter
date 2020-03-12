from __future__ import absolute_import
from celery import Celery
from celery.bin import worker
app = Celery('twitter-crawler',
             broker='pyamqp://guest@142.93.170.234',
             include=['TrollHunter.twitter_crawler.twint_api.request_twint'])
def run():
    worker_celery = worker.worker(app=app)
    option = {'loglevel': 'INFO'}
    worker_celery.run(**option)
    # app.start(["-A", "request", "worker", "--loglevel","info"])

if __name__ == '__main__':
    run()