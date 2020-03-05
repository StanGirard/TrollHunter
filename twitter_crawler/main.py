from flask import Flask, request
from multiprocessing.dummy import Pool, Manager

from twitter_crawler.twint_api.request import get_info_from_user, get_tweet_from_search, get_origin_tweet

app = Flask(__name__)
# api = Api(app)
pool = Pool(processes=15)
manager = Manager()
queue_data = manager.Queue()


@app.route('/tweets/<string:user>', methods=['GET'])
def user_tweet(user):

    get_info_from_user(user,request.args)
    return "200"


@app.route('/tweets/', methods=['GET'])
def search_tweet():
   return get_tweet_from_search(request.args)

@app.route('/tweets/origin/', methods=['GET'])
def origin_tweet():
    return get_origin_tweet(request.args)



if __name__ == '__main__':
    app.run()
