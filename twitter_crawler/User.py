import pandas as pd
class User:
    def __init__(self,username):
        self.username = username
        self.info_df = None
        self.follow_df = None


    def set_info_to_df(self,user_obj):
        self.info_df = pd.DataFrame.from_dict([vars(user_obj)])

    def set_follower_df(self,follow):
        self.follower_df = follow

    def set_following_df(self,follow):
        self.following_df = follow

    def set_tweet_df(self,tweet):
        self.tweets_df = tweet

    def set_follow_df(self, follow):
        if self.follow_df is None:
            self.follow_df = pd.DataFrame.copy(follow)
        else:
            self.follow_df = pd.concat([self.follow_df, follow], join="inner")


