import twint
## pip3 install twint
## Check doc if needed https://doc.trollhunter.guru/twint_install.html
config = twint.Config()
config.Username = "mus_mastour"
config.User_full = True
config.Profile_full = True
config.Pandas_au = True
config.Store_object = True
# twint.run.Search(config)
twint.run.Lookup(config)
# twint.run.Profile(config)
tweets_result_df = twint.output.panda.Tweets_df

print(twint.output)
