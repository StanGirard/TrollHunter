import pandas as pd
class User:
    def __init__(self,username):
        self.username = username


    def set_info_to_df(self,user_obj):
        self.info_df = pd.DataFrame.from_dict([vars(user_obj)])

    def set_follower_df(self,follow):
        self.follower_df = follow

    def set_following_df(self,follow):
        self.following_df = follow
