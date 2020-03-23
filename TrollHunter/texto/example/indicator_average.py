import pandas as pd
import os
from Sentiment import get_sentiment_value, get_polarity_value, get_subjectivity_value
import warnings

warnings.simplefilter(action='ignore')


class Indicator:
    def __init__(self, data_folder):
        self.data_folder = data_folder

    @staticmethod
    def average(values_tab):
        return sum(values_tab) / len(values_tab)

    @staticmethod
    def get_indicators_user(user_file):
        df_csv = pd.read_csv(user_file)

        tweet_list = df_csv[["text"]]

        tweet_list['sentiment'] = tweet_list['text'].apply(get_sentiment_value)
        tweet_list['polarity'] = tweet_list['text'].apply(get_polarity_value)
        tweet_list['subjectivity'] = tweet_list['text'].apply(get_subjectivity_value)

        average_sentiment = tweet_list['sentiment'].mean()
        average_polarity = tweet_list['polarity'].mean()
        average_subjectivity = tweet_list['subjectivity'].mean()

        return average_sentiment, average_polarity, average_subjectivity

    def get_all_indicator_users(self):
        average_sentiment = []
        average_polarity = []
        average_subjectivity = []

        cpt = 1
        for element in os.listdir(self.data_folder):
            if not os.path.isdir(element):
                sentiment, polarity, subjectivity = self.get_indicators_user(os.path.join(self.data_folder, element))
                average_sentiment.append(sentiment)
                average_polarity.append(polarity)
                average_subjectivity.append(subjectivity)
                cpt += 1

        average_sentiment = self.average(average_sentiment)
        average_polarity = self.average(average_polarity)
        average_subjectivity = self.average(average_subjectivity)

        return average_sentiment, average_polarity, average_subjectivity


if __name__ == '__main__':
    indi = Indicator('./users-tweets')
    print(indi.get_all_indicator_users())
