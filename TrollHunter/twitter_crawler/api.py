import time
from datetime import date
from multiprocessing.dummy import Value, Process
from threading import Thread
from flask import Flask, request, Response

from TrollHunter.twitter_crawler import crawler
from TrollHunter.twitter_crawler.twint_api import request_twint

app = Flask(__name__)
p = None
_stop = Value('b',False)

@app.route('/tweets/<string:user>', methods=['GET'])
def user_tweet(user):
    request_twint.get_info_from_user.delay(user, request.args)
    return "200"



@app.route('/tweets/', methods=['GET'])
def search_tweet():

    global p
    global _stop

    if not _stop.value:
        return  " please stop previous search wiht endpoint /stop"
    else:
        _stop.value = False


    p = Process(target=crawl,args=(request.args,_stop))
    p.start()

    return "200"




@app.route('/stop/', methods=['GET'])
def stop():
    global _stop
    _stop.value = True
    return "200"


@app.route('/tweets/origin/', methods=['GET'])
def origin_tweet():
    return request_twint.get_origin_tweet.delay(request.args)

def crawl(args,stop):
    now = date.today()
    print('Start crawler twitter')
    while not stop.value:
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
    print("Stop crawl")

def run():
    app.run()

if __name__ == '__main__':
    run()
