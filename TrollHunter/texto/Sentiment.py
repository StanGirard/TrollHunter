from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import pandas as pd


def get_sentiment_from_tweets(tweet):
    if not isinstance(tweet, list):
        tweet = [tweet]

    analyser = SentimentIntensityAnalyzer()
    sentiment_scores = []

    for t in tweet:
        score = analyser.polarity_scores(t)
        score['tweet'] = t
        sentiment_scores.append(score)

    sentiment_df = pd.DataFrame(sentiment_scores)

    return sentiment_df


def get_sentiment_value(tweet):
    analyser = SentimentIntensityAnalyzer()

    score = analyser.polarity_scores(tweet)

    return score['compound']


def get_polarity(tweet):
    if not isinstance(tweet, list):
        tweet = [tweet]

    tab_result = {'tweet': [],
                  'polarity': []}

    for t in tweet:
        obj = TextBlob(t)
        polarity = obj.sentiment.polarity

        tab_result['tweet'].append(t)
        tab_result['polarity'].append(polarity)

    df_result = pd.DataFrame(tab_result, columns=['tweet', 'polarity'])

    return df_result


def get_polarity_value(tweet):
    obj = TextBlob(tweet)
    polarity = obj.sentiment.polarity

    return polarity


def get_subjectivity(tweet):
    if not isinstance(tweet, list):
        tweet = [tweet]

    tab_result = {'tweet': [],
                  'subjectivity': []}

    for t in tweet:
        obj = TextBlob(t)
        subjectivity = obj.sentiment.subjectivity

        tab_result['tweet'].append(t)
        tab_result['subjectivity'].append(subjectivity)

    df_result = pd.DataFrame(tab_result, columns=['tweet', 'subjectivity'])

    return df_result


def get_subjectivity_value(tweet):
    obj = TextBlob(tweet)
    subjectivity = obj.sentiment.subjectivity

    return subjectivity


if __name__ == '__main__':
    tweets = ["I'm so happy", "I surprised him", "It's a sad news", "I'm happy and sad at the same time"]
    sentiment = get_sentiment_from_tweets(tweets)
    polarity = get_polarity(tweets)
    sub = get_subjectivity(tweets)

    print("SENTIMENT\n", sentiment, "\n")
    print("POLARITY\n", polarity, "\n")
    print("SUBJECTIVITY\n", sub, "\n")
