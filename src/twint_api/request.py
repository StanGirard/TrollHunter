import twint
import datetime
import dateutil


config = twint.Config()

def get_list_tweets(config,args):

    get_twint_config(config,args)
    twint.output.tweets_list.clear()
    twint.run.Search(config)
    return twint.output.tweets_list

def get_tweet_from_user(user,args):
    config.Username = user
    config.Search = None
    get_twint_config(config,args)
    tweets_result = get_list_tweets(config,args)

    return format_tweet_to_html(tweets_result,user)

def get_tweet_from_search(args):
    config.Username = None
    if not "search" in args:
        return " bad request"
    config.Search = args["search"]
    tweet_result = get_list_tweets(config,args)
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

