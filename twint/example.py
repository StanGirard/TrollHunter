import twint
## pip3 install twint
## Check doc if needed https://doc.trollhunter.guru/twint_install.html
c = twint.Config()
c.Search = "fruit"
c.Output = "tweets.csv"
c.Store_csv = True
c.Min_likes = 10
c.Limit = 100
c.Lang = "en"
twint.run.Search(c)
