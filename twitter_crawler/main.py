from flask import Flask, request

from twitter_crawler.twint_api.request import get_info_from_user, get_tweet_from_search, get_origin_tweet

app = Flask(__name__)


@app.route('/tweets/<string:user>', methods=['GET'])
def user_tweet(user):
    get_info_from_user.delay(user, request.args)
    return "200"


@app.route('/tweets/', methods=['GET'])
def search_tweet():
    return get_tweet_from_search.delay(request.args)


@app.route('/tweets/origin/', methods=['GET'])
def origin_tweet():
    return get_origin_tweet.delay(request.args)


if __name__ == '__main__':
    app.run()
