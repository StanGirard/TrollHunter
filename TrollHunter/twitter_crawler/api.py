import time
from datetime import date

from flask import Flask, request

from TrollHunter.twitter_crawler import crawler
from TrollHunter.twitter_crawler.twint_api import request_twint

app = Flask(__name__)
stop = False


@app.route('/tweets/<string:user>', methods=['GET'])
def user_tweet(user):
    request_twint.get_info_from_user.delay(user, request.args)
    return "200"


@app.route('/tweets/', methods=['GET'])
def search_tweet():
    yield "200"
    now = date.today()
    args = request.args
    print('Start crawler twitter')
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

@app.route('/stop/', methods=['GET'])
def stop():
    global stop
    stop = True
    return "200"


@app.route('/tweets/origin/', methods=['GET'])
def origin_tweet():
        return request_twint.get_origin_tweet.delay(request.args)


def run():
    app.run()

if __name__ == '__main__':
    run()
