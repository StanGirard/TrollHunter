import pandas as pd
class User:
    def __init__(self,username):
        self.username = username
        self.info_df = None
        self.info_follow_df = None
        self.interaction_df = None


    def set_info_to_df(self,user_obj):
        self.info_df = pd.DataFrame.from_dict([vars(user_obj)])

    def set_follower_df(self, follow):
        self.follower_df = follow

    def set_following_df(self, follow):
        self.following_df = follow

    def set_tweet_df(self,tweet):
        self.tweets_df = tweet

    def set_follow_df(self, follow, follower_id, following_id):
        if self.info_follow_df is None:
            self.info_follow_df = pd.DataFrame.copy(follow)
        else:
            self.info_follow_df = pd.concat([self.info_follow_df, follow], join="inner")
        self.set_interaction(follower_id, "follow", following_id)

    def set_interaction(self, user_a, interaction, usr_b):
        if self.interaction_df is None:
            self.interaction_df = pd.DataFrame(columns=["id", "follower", "interaction", "following"])
        self.interaction_df = self.interaction_df.append({
            "id": str(user_a) + "_" + str(usr_b),
            'follower': user_a,
            'interaction': interaction,
            'following': usr_b
        }, ignore_index=True)




