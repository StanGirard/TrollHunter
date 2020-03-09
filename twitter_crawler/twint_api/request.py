import datetime
from twitter_crawler.twint import twint
from twitter_crawler.User import User
from twitter_crawler.tweet_obj import Tweet_obj
from twitter_crawler.celeryapp import app

config = twint.Config()

@app.task
def get_info_from_user(username, args):
    user = User(username)
    config.Username = user.username

    get_twint_config(config,args)

    get_info_user(user,config)
    get_follower_user(user,config,args)
    get_following_user(user,config,args)

    get_tweet_from_user(user,config,args)

    return "user"

@app.task
def get_follower_user(user, args):
    get_twint_config(args)
    config.Username = user.username
    config.Followers = True
    config.Pandas_au = True
    config.User_full = False
    config.Store_object = True
    config.Limit = user.info_df.loc[0]["followers"]
    twint.run.Followers(config)
    user.set_follower_df(twint.output.panda.Follow_df)


@app.task
def get_following_user(user,  args):
    get_twint_config( args)
    config.Username = user.username
    config.Pandas_au = True
    config.User_full = False
    config.Store_object = True
    config.Limit = user.info_df.loc[0]["following"]
    twint.run.Following(config)
    user.set_following_df(twint.output.panda.Follow_df)


@app.task
def get_info_user(user):
    config.Username = user.username
    config.User_full = True
    config.Profile_full = True
    config.Pandas = False
    config.Store_object = True
    config.Since = datetime.date.today().isoformat()
    # Need Lookup because bug with twint and flask
    twint.run.Search(config)
    twint.run.Lookup(config)
    user.set_info_to_df(twint.output.users_list[0])


@app.task
def get_list_tweets(  args):
    get_twint_config( args)
    config.Profile = True
    config.Profile_full = True
    twint.output.tweets_list.clear()
    twint.run.Profile(config)
    # twint.output.panda.Tweets_df.to_json("./test.json")
    return twint.output.tweets_list


@app.task
def get_tweet_from_user(user,args,):
    # print("test")
    get_twint_config(args)
    config.Search = None
    tweets_result = get_list_tweets(config, args)
    user.set_tweet_df(twint.output.panda.Tweets_df)

    return format_tweet_to_html(tweets_result, user.username)


@app.task
def get_tweet_from_search(args):
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
    get_twint_config(config,args)
    tweet = args["search"]
    config.Username = None
    config.Store_object = True
    config.Search = tweet

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


def get_twint_config( args):
    limit = 100
    since = None
    retweet = False
    until = None
    if "limit" in args:
        limit = int(args["limit"])
    if "since" in args:
        since = args["since"]
    if "until" in args:
        until = args["until"]
    if "retweet" in args:
        retweet = args["retweet"].lower() == "true"

    if "search" in args:
        config.Search = args["search"]
    config.Limit = limit
    config.Retweets = retweet
    config.Since = since
    config.Until = until
    config.Pandas = True
    config.Store_object = True


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
