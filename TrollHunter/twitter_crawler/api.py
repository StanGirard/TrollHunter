import time
from datetime import date

from flask import Flask, request

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

"""get tweets/follow interaction from user"""
@app.route('/tweets/<string:user>', methods=['GET'])
def user_tweet(user):
    request_twint.get_info_from_user.delay(user, request.args)
    return "200"

"""get many tweets from hashtag or search terms"""
@app.route('/tweets/', methods=['GET'])
def search_tweet():
    yield "200"
    now = date.today()
    args = request.args
    print('Start crawler twitter')
    # sleep 2 hours and crawl tweet since 2hour
    while not stop:
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

"""stop search"""
@app.route('/stop/', methods=['GET'])
def stop():
    global stop
    stop = True
    return "200"

"""get origin of a tweet"""
@app.route('/tweets/origin/', methods=['GET'])
def origin_tweet():
        return request_twint.get_origin_tweet.delay(request.args)


def run():
    app.run()

if __name__ == '__main__':
    run()
