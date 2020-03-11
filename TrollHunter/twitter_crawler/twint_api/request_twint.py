import datetime
import pandas as pd
from TrollHunter.twitter_crawler.User import User
from TrollHunter.twitter_crawler.tweet_obj import Tweet_obj
from TrollHunter.twitter_crawler.celeryapp import app
from TrollHunter.twitter_crawler.elastic import Elastic
from TrollHunter.twitter_crawler.twint import twint

HIDE_TWEET_OUPUT = True
elastic = Elastic()

"""
args:
    tweet:          set to 0 to avoid tweet (default: 1)
    follow:         set to 0 to avoid follow (default: 1)
    limit:          set the number of tweet to retrieve (Increments of 20, default: 100)
    follow_limit    set the number of following and followers to retrieve 
    since:          date selector for tweets (Example: 2017-12-27)
    until:          date selector for tweets (Example: 2017-12-27)
    retweet:        set to 1 to retrieve retweet (default: 0)
    search:         search terms
    
TODO: Retrieve tweet twitted to the user ?
"""
@app.task
def get_info_from_user(username, args):
    reset_data()
    user = User(username)

    get_info_user(user, args)
    # elastic.store_users(user.info_df)

    if "tweet" not in args or int(args["tweet"]) == 1:
        get_tweet_from_user(user, args)
        # elastic.store_tweets(user.tweets_df)

    if "follow" not in args or int(args["follow"]) == 1:
        get_follower_user(user, args)
        get_following_user(user, args)
        # elastic.store_users(user.info_follow_df)
        # elastic.store_interaction(user.interaction_df)

    return "user"


def get_follower_user(user, args):
    config = get_twint_config(args, user=user)
    config.Pandas_au = True
    config.User_full = False
    if "follow_limit" in args:
        config.Limit = int(args["follow_limit"])
    else:
        config.Limit = user.info_df.loc[0]["followers"]
    twint.run.Followers(config)
    user.set_follower_df(twint.output.panda.Follow_df)
    i = 1
    limit = config.Limit
    for username in user.follower_df.iloc[0]['followers']:
        follower = User(username)
        get_info_user(follower, args)
        user.set_follow_df(follower.info_df, follower.info_df.loc[0]['id'], user.info_df.loc[0]['id'])
        print("Processed ", i, "/", limit, " followers")
        i += 1


def get_following_user(user, args):
    config = get_twint_config(args, user=user)
    config.Pandas_au = True
    config.User_full = False
    if "follow_limit" in args:
        config.Limit = int(args["follow_limit"])
    else:
        config.Limit = user.info_df.loc[0]["following"]
    twint.run.Following(config)
    user.set_following_df(twint.output.panda.Follow_df)
    i = 1
    limit = config.Limit
    for username in user.following_df.iloc[0]['following']:
        following = User(username)
        get_info_user(following, args)
        user.set_follow_df(following.info_df, user.info_df.loc[0]['id'], following.info_df.loc[0]['id'])
        print("Processed ", i, "/", limit, " following")
        i += 1

def get_info_user(user, args):
    config = get_twint_config(args, user=user)
    config.User_full = True
    config.Profile_full = True
    config.Pandas = False
    config.Since = datetime.date.today().isoformat()
    # Need Lookup because bug with twint and flask
    twint.run.Search(config)
    twint.run.Lookup(config)
    user.set_user_id(config.User_id)
    user.set_info_to_df(twint.output.users_list[-1])


def get_tweet_from_user(user, args):
    config = get_twint_config(args, user=user)
    config.Profile = True
    config.Profile_full = True
    twint.output.tweets_list.clear()
    twint.run.Profile(config)
    user.set_tweet_df(twint.output.panda.Tweets_df)
    return twint.output.tweets_list


@app.task
def get_tweet_from_search(args):
    config = twint.Config()
    config.Username = None
    config.Store_object = True
    if not "search" in args:
        return " bad request"
    config.Search = args["search"]
    twint.output.tweets_list.clear()
    twint.run.Search(config)
    tweet_result = twint.output.tweets_list

    tweets_result_df = twint.output.panda.Tweets_df

    return format_tweet_to_html(tweet_result, "test")


@app.task
def get_origin_tweet(args):
    if "search" not in args:
        return " bad request"
    tweet = args["search"]

    config = get_twint_config(args)

    twint.output.tweets_list.clear()
    twint.run.Search(config)

    tweets = twint.output.tweets_list

    tweet_result = reversed([Tweet_obj(t) for t in tweets])
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
        config.User_id = user.user_id

    if "limit" in args:
        config.Limit = int(args["limit"])
    else:
        config.Limit = 100

    if "since" in args:
        config.Since = args["since"]
    if "until" in args:
        config.Until = args["until"]
    if "retweet" in args:
        config.Retweets = args["retweet"].lower() == "true"
    if "search" in args:
        config.Search = args["search"]

    config.Pandas = True
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
