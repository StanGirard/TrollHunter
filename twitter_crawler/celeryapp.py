from __future__ import absolute_import
from celery import Celery

app = Celery('twitter-crawler',
             broker='pyamqp://guest@142.93.170.234',
             include=['twint_api.tasks'])

