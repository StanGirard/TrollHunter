import time
from datetime import date
from multiprocessing.dummy import Value, Process
from threading import Thread
from flask import Flask, request, Response

from TrollHunter.twitter_crawler import crawler
from TrollHunter.twitter_crawler.twint_api import request_twint

app = Flask(__name__)
stop = False
"""
args:
    tweet:          set to 0 to avoid tweet (default: 1)
    follow:         set to 0 to avoid follow (default: 1)
    limit:          set the number of tweet to retrieve (Increments of 20, default: 100)
    follow_limit:   set the number of following and followers to retrieve (default: 100)
    since:          date selector for tweets (Example: 2017-12-27)
    until:          date selector for tweets (Example: 2017-12-27)
    retweet:        set to 1 to retrieve retweet (default: 0)
    search:         search terms format "i search"
                    for hashtag : (#Hashtag)
                    for multiple : (#Hashtag1 AND|OR #Hashtag2)
                    
    tweet_interact: set to 1 to parse tweet interaction between users (default: 0)
    depth:          search tweet and info from list of follow

TODO: Retrieve tweet twitted to the user ?
"""
p = None
_stop = Value('b',True)

"""get tweets/follow interaction from user"""
@app.route('/tweets/<string:user>', methods=['GET'])
def user_tweet(user):
    request_twint.get_info_from_user.delay(user, request.args)
    return "200"

"""get many tweets from hashtag or search terms"""
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



"""stop search"""
@app.route('/stop/', methods=['GET'])
def stop():
    global _stop
    _stop.value = True
    return "200"

"""get origin of a tweet"""
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

def run(port=6000):
    app.run(port=port)

if __name__ == '__main__':
    run()
