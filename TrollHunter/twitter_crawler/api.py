from flask import Flask, request

from TrollHunter.twitter_crawler import crawler
from TrollHunter.twitter_crawler.twint_api import request_twint

app = Flask(__name__)



@app.route('/tweets/<string:user>', methods=['GET'])
def user_tweet(user):
    request_twint.get_info_from_user(user, request.args)
    return "200"


@app.route('/tweets/', methods=['GET'])
def search_tweet():
    crawler.crawl_from_search.delay(request.args)
    # request_twint.get_tweet_from_search.delay(request.args)
    return "200"


@app.route('/tweets/origin/', methods=['GET'])
def origin_tweet():
        return request_twint.get_origin_tweet.delay(request.args)


def run():
    app.run()

if __name__ == '__main__':
    run()
