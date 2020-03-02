import pandas as pd
class User:
    def __init__(self,username):
        self.username = username


    def set_info_to_df(self,user_obj):
        self.user_info_df = pd.DataFrame.from_dict([vars(user_obj)])
        print(self.user_info_df)
