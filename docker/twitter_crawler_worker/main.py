from TrollHunter.twitter_crawler import celeryapp

if __name__ == "__main__":
    celeryapp.run_crawler()

