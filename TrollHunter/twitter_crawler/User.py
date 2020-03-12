import pandas as pd
class User:
    def __init__(self,username):
        self.username = username
        self.info_df = None
        self.info_actor_df = None
        self.interaction_df = None
        self.user_id = None
        self.tweets_df = None
        self.interaction_set = set()


    def set_info_to_df(self,user_obj):
        self.info_df = pd.DataFrame.from_dict([vars(user_obj)])

    def set_user_id(self, user_id):
        self.user_id = user_id

    def set_follower_df(self, follow):
        self.follower_df = follow

    def set_following_df(self, follow):
        self.following_df = follow

    def set_tweet_df(self,tweet):
        self.tweets_df = tweet

    def extract_tweet_interaction(self, tweets):
        usrname = set()
        self.init_interaction()
        for tweet in tweets:
            if tweet.user_rt:
                usrname.add(tweet.username)
                self.add_interaction(
                    str(tweet.conversation_id) + str(tweet.user_id) + str(tweet.user_rt_id),
                    tweet.user_rt_id,
                    'retweet',
                    tweet.user_id,
                    source=tweet.id
                )
            else:
                for usr in tweet.reply_to:
                    if int(tweet.user_id) != int(usr['user_id']):
                        usrname.add(usr['username'])
                        self.add_interaction(
                            str(tweet.conversation_id) + str(tweet.user_id) + str(usr['user_id']),
                            tweet.user_id,
                            'converse',
                            usr['user_id'],
                            source=tweet.id
                        )
        return usrname

    def add_actor_info(self, actor):
        if self.info_actor_df is None:
            self.info_actor_df = pd.DataFrame.copy(actor)
        else:
            self.info_actor_df = pd.concat([self.info_actor_df, actor], join="inner")

    def set_follow_df(self, follow, follower_id, following_id):
        self.add_actor_info(follow)

        self.add_interaction(
            str(follower_id) + str(following_id),
            follower_id,
            "follow",
            following_id)

    def add_interaction(self, id, twittos_a, interaction, twittos_b, source=''):
        if id in self.interaction_set:
            return
        self.interaction_set.add(id)
        self.interaction_df = self.interaction_df.append({
            'id': id,
            'twittos_a': str(twittos_a),
            'interaction': interaction,
            'twittos_b': str(twittos_b),
            'source': str(source)
        }, ignore_index=True)

    def init_interaction(self):
        if self.interaction_df is None:
            self.interaction_df = pd.DataFrame(columns=["id", "twittos_a", "interaction", "twittos_b"])
