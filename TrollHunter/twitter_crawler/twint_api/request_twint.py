import datetime
import pandas as pd
import json
from TrollHunter.twitter_crawler import crawler
from TrollHunter.twitter_crawler.celeryapp import app
from TrollHunter.twitter_crawler.twint_api.user import User, Crawled
from TrollHunter.twitter_crawler.twint_api.tweetobj import TweetObj
from TrollHunter.twitter_crawler.twint_api.elastic import Elastic
from TrollHunter.twitter_crawler.twint import twint

HIDE_TWEET_OUPUT = True
elastic = Elastic()

"""
args:
    tweet:          set to 0 to avoid tweet (default: 1)
    follow:         set to 0 to avoid follow (default: 1)
    limit:          set the number of tweet to retrieve (Increments of 20, default: 100)
    follow_limit:   set the number of following and followers to retrieve (default: 100)
    since:          date selector for tweets (Example: 2017-12-27)
    until:          date selector for tweets (Example: 2017-12-27)
    retweet:        set to 1 to retrieve retweet (default: 0)
    search:         search terms
    tweet_interact: set to 1 to parse tweet interaction between users (default: 0)
    depth:          search tweet and info from list of follow
    
TODO: Retrieve tweet twitted to the user ?
"""
@app.task
def get_info_from_user(username, args):
    reset_data()
    user = User(username)

    get_info_user(user, args)
    elastic.store_crawled(user.user_info)
    elastic.store_user(user.user_info)

    get_user_interaction(args, user)


def get_user_interaction(args,user):
    if "tweet" not in args or int(args["tweet"]) == 1:
        get_tweet_from_user(user, args)
        elastic.store_tweets(user.tweets)

        if "tweet_interact" in args and int(args["tweet_interact"]) == 1:
            retrieve_tweet_actors(user, args)

    if "follow" not in args or int(args["follow"]) == 1:
        get_follower_user(user, args)
        get_following_user(user, args)

    elastic.store_users(user.actors_info)
    if "depth" in args and int(args["depth"]) > 0:
        crawler.crawl.delay(json.dumps(list(user.actors)), args)

    elastic.store_interactions(user.interactions)
    return "user"


def retrieve_tweet_actors(user, args):
    tweet_users = user.extract_tweet_interaction()
    i = 1
    for tweet_user in tweet_users:
        tweet_user = User(tweet_user)
        get_info_user(tweet_user, args)
        user.add_actor_info(tweet_user.user_info)
        print("Processed", i, "/", len(tweet_users), "tweet actors")
        i += 1


def get_follower_user(user, args):
    config = init_follow_retrieval(user, args)
    twint.run.Followers(config)
    i = 1
    limit = config.Limit
    for username in twint.output.follows_list:
        follower = User(username)
        get_info_user(follower, args)
        user.set_follow(follower.user_info, follower.user_info.id, user.user_info.id)
        print("Processed", i, "/", limit, "followers")
        i += 1


def get_following_user(user, args):
    config = init_follow_retrieval(user, args)
    twint.run.Following(config)
    i = 1
    limit = config.Limit
    for username in twint.output.follows_list:
        following = User(username)
        get_info_user(following, args)
        user.set_follow(following.user_info, user.user_info.id, following.user_info.id)
        print("Processed", i, "/", limit, "following")
        i += 1


def init_follow_retrieval(user, args):
    config = get_twint_config(args, user=user)
    config.User_full = False
    if "follow_limit" in args and int(args["follow_limit"]) > -1:
        config.Limit = int(args["follow_limit"])
    else:
        config.Limit = 100
    twint.output.follows_list = []
    return config


def get_info_user(user, args):
    config = get_twint_config(args, user=user)
    config.User_full = True
    config.Profile_full = True
    config.Since = datetime.date.today().isoformat()
    # Need Lookup because bug with twint and flask
    twint.run.Search(config)
    twint.run.Lookup(config)
    user.set_user_info(twint.output.users_list[-1])


def get_tweet_from_user(user, args):
    config = get_twint_config(args, user=user)

    config.Profile = True
    config.Profile_full = True
    twint.output.tweets_list.clear()
    twint.run.Profile(config)
    user.set_tweets(twint.output.tweets_list)
    return user.tweets


@app.task
def get_tweet_from_search(args):
    config = twint.Config()
    config.Store_object = True
    if not "search" in args:
        return " bad request"
    config.Search = args["search"]
    twint.output.tweets_list.clear()
    twint.run.Search(config)
    tweet_result = twint.output.tweets_list

    return format_tweet_to_html(tweet_result, "test")

def crawl_tweet(args):
    reset_data()
    config = get_twint_config(args)
    twint.run.Search(config)
    return  twint.output.tweets_list


@app.task
def get_origin_tweet(args):
    if "search" not in args:
        return " bad request"
    tweet = args["search"]

    config = get_twint_config(args)

    twint.output.tweets_list.clear()
    twint.run.Search(config)

    tweets = twint.output.tweets_list

    tweet_result = reversed([TweetObj(t) for t in tweets])
    origin = None

    for t in tweet_result:
        if t.check_equal(tweet):
            origin = t
            break

    res = []

    if origin:
        origin.pretty_print()
        res.append(origin)

    return format_tweet_to_html(res, "ORIGIN")


def get_twint_config(args, user=None):
    config = twint.Config()
    config.Hide_output = HIDE_TWEET_OUPUT
    if user is not None:
        config.Username = user.username
        if user.user_info is not None:
            config.User_id = user.user_info.id

    if "limit" in args:
        config.Limit = int(args["limit"])
    else:
        config.Limit = 100

    if "since" in args:
        config.Since = args["since"]
    if "until" in args:
        config.Until = args["until"]
    if "retweet" in args:
        config.Retweets = bool(int(args["retweet"]) == 1)  # Do not convert directly form str to bool
    if "search" in args:
        config.Search = args["search"]

    config.Store_object = True
    return config


def format_tweet_to_html(tweets_list, word):
    ret = "<h1>tweet from {} </h1><br>".format(word)
    for tweet in tweets_list:
        ret += "date : {},  username : {}, name : {} like : {}, retweets count = {}, tweet : {} <br>".format(
            tweet.datestamp + ":" + tweet.timestamp,
            tweet.username,
            tweet.name,
            tweet.likes_count,
            tweet.retweets_count,
            tweet.tweet
        )
    return ret


def reset_data():
    twint.output.tweets_list.clear()
    twint.output.users_list.clear()
