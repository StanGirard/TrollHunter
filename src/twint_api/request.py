import twint
import datetime
import dateutil
import asyncio
from multiprocessing.dummy import Pool,Manager




config = twint.Config()

def get_info_from_user(user,args):
    # get_twint_config(config,args)
    user_info = get_info_user(user,config)


    # return format_tweet_to_html(tweets_result,user)

def get_info_user(user,config):
    config.Username = "mus_mastour"
    config.User_full = True
    config.Profile_full = True
    config.Pandas_au = True
    config.Store_object = True
    config.Since = datetime.date.today().isoformat()
    # Need Lookup because bug with twint and flask
    twint.run.Search(config)
    twint.run.Lookup(config)
    # twint.run.Profile(config)
    tweets_result_df = twint.output.panda.Tweets_df

    print(twint.output)
    return 0

def get_list_tweets(config,args):

    get_twint_config(config,args)
    twint.output.tweets_list.clear()
    twint.run.Search(config)
    # twint.output.panda.Tweets_df.to_json("./test.json")
    return twint.output.tweets_list


def get_tweet_from_user(user,args):
    # print("test")
    config.Username = user
    config.Search = None
    get_twint_config(config,args)
    tweets_result = get_list_tweets(config,args)
    tweets_result_df = twint.output.panda.Tweets_df
    return format_tweet_to_html(tweets_result,user)

def get_tweet_from_search(args):
    config.Username = None
    if not "search" in args:
        return " bad request"
    config.Search = args["search"]
    tweet_result = get_list_tweets(config,args)
    tweets_result_df = twint.output.panda.Tweets_df

    return format_tweet_to_html(tweet_result,"test")



def get_twint_config(config,args):
    limit = 100
    since = datetime.date.today() - datetime.timedelta(days=10)
    since = since.isoformat()
    retweet = False

    if "limits" in args:
        limit = args["limits"]
    if "since" in args:
        since = args["since"]
    if "retweet" in args:
        retweet = args["retweet"]
    if "search" in args:
        config.Search = args["search"]

    config.Limit = limit
    config.Retweets = retweet
    config.Since = since
    config.Pandas = True
    config.Store_object = True

def format_tweet_to_html(tweets_list,word):
    ret = "<h1>tweet from {} </h1><br>".format(word)
    for tweet in tweets_list:
        ret += "date : {},  username : {}, name : {} like : {}, retweets count = {}, tweet : {} <br>".format(
            tweet.datestamp+":"+tweet.timestamp,
            tweet.username,
            tweet.name,
            tweet.likes_count,
            tweet.retweets_count,
            tweet.tweet
        )
    return ret

