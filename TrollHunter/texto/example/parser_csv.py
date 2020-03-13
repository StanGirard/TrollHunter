import pandas as pd


def get_user_data(user_file):
    df_csv = pd.read_csv(user_file)

    result = df_csv[["id", "followers_count", "description"]]

    return result


def get_tweet_data(tweet_file):
    df_csv = pd.read_csv(tweet_file)

    result = df_csv[["user_id", "retweet_count", "retweeted", "favorite_count", "text", "hashtags", "mentions"]]

    return result


def find_tweets_from_user(df_tweets, id_user):
    result = df_tweets.loc[df_tweets["user_id"] == id_user]

    return result


if __name__ == '__main__':
    p = get_tweet_data("./russian-troll-tweets/tweets.csv")
    t = find_tweets_from_user(p, 1510488662)
    print(t)
