import unidecode

skip_charac = ["\"", "\'", "\n"]


class TweetObj:
    def __init__(self, tweet):
        self.datestamp = tweet.datestamp
        self.timestamp = tweet.timestamp
        self.date = tweet.datestamp + ":" + tweet.timestamp
        self.username = tweet.username
        self.name = tweet.name
        self.likes_count = tweet.likes_count
        self.retweets_count = tweet.retweets_count
        self.tweet = tweet.tweet

    def check_equal(self, tweet):
        return self.tweet_cleaner(self.tweet) == self.tweet_cleaner(tweet)

    def pretty_print(self):
        print("DATE : {} \n USER : {} \n TWEET : {}".format(self.date, self.username, self.tweet))

    @staticmethod
    def tweet_cleaner(tweet):
        result = unidecode.unidecode(tweet)
        for c in skip_charac:
            result = result.replace(c, '')

        return result.lower()
