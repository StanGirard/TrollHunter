import pandas as pd
from polyglot.detect import Detector


def get_user_data(user_file):
    df_csv = pd.read_csv(user_file)

    result = df_csv[["id", "followers_count", "description"]]

    return result


def get_tweet_data(tweet_file):
    df_csv = pd.read_csv(tweet_file)

    result = df_csv[["user_id", "retweet_count", "retweeted", "favorite_count", "text", "hashtags", "mentions",
                     "created_at", "created_str"]]

    return result


def find_tweets_from_user(df_tweets, id_user) -> pd.DataFrame:
    result = df_tweets.loc[df_tweets["user_id"] == id_user]

    return result


if __name__ == '__main__':
    p = get_tweet_data("./tweets.csv")
    users = pd.read_csv("./users.csv")
    begPath = "./users-tweets/"

    tweetList = []

    for id in users['id'].values:
        try:
            intId = int(id)
            file = begPath + "user_" + str(intId) + ".csv"
            t = find_tweets_from_user(p, intId)
            t = t.sort_values(by="created_at", ascending=True)
            textValues = t['text'].values

            # check language
            cptWrongLang = 0
            for text in textValues:
                main_language = Detector(text).language
                if main_language.code != "en":
                    cptWrongLang += 1

            if cptWrongLang / len(textValues) > 0.2:
                continue

            tweetList.append(pd.DataFrame(textValues))
            t.to_csv(file, index=False)
        except:
            print("exception")
            continue

    tweets = pd.concat(tweetList)
    tweets.to_csv("./new_tweets", index=False)
