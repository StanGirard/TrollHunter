import pandas as pd
import numpy as np
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import OneClassSVM
from sklearn.cluster import KMeans
import sys
from scipy.sparse import csr_matrix, hstack

sys.path.append('../')
from Sentiment import get_sentiment_from_tweets, get_polarity, get_subjectivity
from Keyword import lemetize_text

# https://medium.com/@0xskywalker/analysis-of-russian-troll-farm-using-anomalous-detection-b56dcdafa9d5

data = "tweets.csv"
read_data = pd.read_csv(data)
read_tweets = read_data['text'].values

#remove bad chars
def cleantext(text):
    #return ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", text).split())
    return ' '.join(re.sub(r"(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)|^RT|http.+?", "", text).split())

#clean text and reduce to lower case
data_size = 15000
processed_tweets = list()
X_train2 = read_tweets[:]
for sentence in read_tweets:
    try:
        processed_tweets.append(lemetize_text(cleantext(sentence).lower()))
    except:
        continue

#convert to numpy array
processed_tweets = np.array(processed_tweets)

#create X_train/X_test
X_train_data = processed_tweets[:data_size]

#X_test = processed_tweets[:data_size]
print("Trainining Data Size:", X_train_data.size)
#print("Test Data Size:", X_test.size)

#apply tf-idf
# récupérér une matrice de d'occurence pondéré de mots par tweet
vectorizer = TfidfVectorizer(use_idf=True)
X_train = vectorizer.fit_transform(X_train_data)
#print(vectorizer.get_feature_names())

""" Process subjectivity, polarity, feelings """

setOffeelings = []
sentiments = get_sentiment_from_tweets(X_train_data).compound.values
subjectivity = get_subjectivity(X_train_data).subjectivity.values
polarity = get_polarity(X_train_data).polarity.values

A = csr_matrix(list(map(lambda x: [x], sentiments)), dtype="float")
B = csr_matrix(list(map(lambda x: [x], subjectivity)), dtype="float")
C = csr_matrix(list(map(lambda x: [x], polarity)), dtype="float")

matrix = hstack([A, B, C])
X_train = hstack([X_train, matrix])

""" End Processing """

#print(pd.DataFrame.sparse.from_spmatrix(X_train))
#X_test = vectorizer.transform(X_test)

model = OneClassSVM(kernel='rbf')
nbIndexes = 2
kModel = KMeans(n_clusters=nbIndexes)
y_train = kModel.fit_predict(X_train)

#model.fit(X_train)
#model.fit(X_test)
#y_train = model.predict(X_train)
#y_test = model.predict(X_test)
#print(y_train)

#number of anomalies
#train = y_train[y_train == 1].size
#test = y_test[y_test == 1].size

indexes = {}
for i in range(0, nbIndexes):
    indexes[i] = list()

for i in range(0, y_train.size):
    goodList = indexes[y_train[i]]
    goodList.append(i)

for index, goodList in indexes.items():
    f = open("index"+str(index)+".txt", "w")
    for i in goodList:
        f.writelines(str(X_train2[i]).strip())
        f.writelines("---------------\n")
    f.close()

#print("Size of inliers in Train set:", train)
#print("Size of inliers in Test set:", test)

#train_anomaly = y_train[y_train == -1].size
#test_anomaly = y_test[y_test == -1].size
#print("Size of outliers in Train set:", train_anomaly)
#print("Size of outliers in Test set:", test_anomaly)
