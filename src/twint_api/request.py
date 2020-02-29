import twint
import datetime
import dateutil

config = twint.Config()

def get_user_tweet(user,args):
    config.Username = user
    limit = 100
    since =  datetime.date.today() - datetime.timedelta(days=10)
    since = since.isoformat()
    retweet = False
    if "limits" in args:
        limit = args["limits"]
    if "since" in args:
        since = args["since"]
    if "retweet" in args:
        retweet = args["retweet"]
    config.Limit = limit
    config.Retweets = retweet
    config.Since = since
    config.Store_object_tweets_list = True
    config.Store_object = True

    twint.run.Search(config)
    tweets_result = twint.output.tweets_list
    return format_tweet_to_html(tweets_result,user)


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

