from flask import Flask, request
from flask_restful import Resource, Api

from twint_api.tasks import get_tweet_from_search, get_tweet_from_user, get_info_from_user

app = Flask(__name__)


# api = Api(app)

@app.route('/tweets/<string:user>', methods=['GET'])
def user_tweet(user):
    get_tweet_from_user.delay(user, request.args)
    return "200"

@app.route('/tweets/', methods=['GET'])
def search_tweet():
    return get_tweet_from_search.delay(request.args)

if __name__ == '__main__':
    app.run()
