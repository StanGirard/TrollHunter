from datetime import datetime


class User:
    def __init__(self, username):
        self.username = username

        self.user_info = None
        self.actors_info = []
        self.interactions = []
        self.tweets = []
        self.actors = set()

    def set_user_info(self, user_info):
        self.user_info = user_info

    def set_tweets(self, tweet):
        self.tweets = tweet

    def extract_tweet_interaction(self):
        usrname = set()
        for tweet in self.tweets:
            if tweet.user_rt:
                usrname.add(tweet.username)
                self.add_interaction(str(tweet.conversation_id) + str(tweet.user_id) + str(tweet.user_rt_id),
                                     tweet.user_rt_id, 'retweet', tweet.user_id, source=tweet.id)
            for usr in tweet.reply_to:
                if int(tweet.user_id) != int(usr['user_id']):
                    usrname.add(usr['username'])
                    self.add_interaction(str(tweet.conversation_id) + str(tweet.user_id) + str(usr['user_id']),
                                         tweet.user_id, 'converse', usr['user_id'], source=tweet.id)
        return usrname

    def add_actor_info(self, actor):
        if actor.username in self.actors:
            return
        self.actors.add(actor.username)
        self.actors_info.append(actor)

    def set_follow(self, follow, follower_id, following_id):
        self.add_actor_info(follow)

        self.add_interaction(str(follower_id) + str(following_id),
                             follower_id, "follow", following_id)

    def add_interaction(self, _id, twittos_a, interaction, twittos_b, source=''):
        self.interactions.append(Interaction(_id, twittos_a, interaction, twittos_b, source))


class Interaction:
    def __init__(self, _id, twittos_a, interaction, twittos_b, source):
        self.id = _id
        self.twittos_a = str(twittos_a)
        self.interaction = interaction
        self.twittos_b = str(twittos_b)
        self.source = str(source)


class Crawled:
    def __init__(self, user):
        self.id = user.id
        self.username = user.username
        self.crawled_time = datetime.now()
