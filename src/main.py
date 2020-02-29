from flask import Flask, request
from flask_restful import Resource, Api

from src.twint_api.request import get_user_tweet

app = Flask(__name__)
api = Api(app)

@app.route('/tweets/<string:user>', methods=['GET'])
def user_tweet(user):

    return get_user_tweet(user,request.args)

    # return "<h1>Distant Reading Archive</h1><p>This site is a prototype API for distant reading of science fiction novels.</p>"
# @app.route('/tweets/')


if __name__ == '__main__':
    app.run(port='5002')
