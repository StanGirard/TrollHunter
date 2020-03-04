class Tweet_obj:
    def __init__(self, tweet):
        self.date = tweet.datestamp + ":" + tweet.timestamp
        self.username = tweet.username
        self.name = tweet.name
        self.like_count = tweet.likes_count
        self.retweets_count = tweet.retweets_count
        self.tweet = tweet.tweet
