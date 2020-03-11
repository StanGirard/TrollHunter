from nltk.sentiment.vader import SentimentIntensityAnalyzer
import pandas as pd


def get_sentiment_from_tweets(tweets):
    analyser = SentimentIntensityAnalyzer()
    sentiment_scores = []

    for t in tweets:
        score = analyser.polarity_scores(t)
        score['tweet'] = t
        sentiment_scores.append(score)

    sentiment_df = pd.DataFrame(sentiment_scores)

    return sentiment_df


if __name__ == '__main__':
    tweets = ["I'm so happy", "I surprised him", "It's a sad news", "I'm happy and sad at the same time"]
    result = get_sentiment_from_tweets(tweets)

    print(result)
