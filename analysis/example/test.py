import pandas as pd
import numpy as np
import re

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import OneClassSVM

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
X_train2 = read_tweets[-data_size:]
for sentence in read_tweets:
    try:
        processed_tweets.append(cleantext(sentence).lower())
    except:
        continue

#convert to numpy array
processed_tweets = np.array(processed_tweets)

#create X_train/X_test
X_train1 = processed_tweets[-data_size:]
X_train = X_train1

X_test = processed_tweets[:data_size]
print("Trainining Data Size:", X_train.size)
print("Test Data Size:", X_test.size)

#apply tf-idf
# récupérér une matrice de d'occurence pondéré de mots par tweet
vectorizer = TfidfVectorizer(use_idf=True)
X_train = vectorizer.fit_transform(X_train)
X_test = vectorizer.transform(X_test)

model = OneClassSVM(kernel='rbf')
model.fit(X_train)
#model.fit(X_test)
y_train = model.predict(X_train)
y_test = model.predict(X_test)

#number of anomalies
train = y_train[y_train == 1].size
test = y_test[y_test == 1].size

indexes1 = list()
indexes2 = list()
for i in range(0, y_train.size):
    if y_train[i] == 1:
        indexes1.append(i)
    else:
        indexes2.append(i)

f = open("minus.txt", "w")
for i in indexes2:
    f.writelines(str(X_train2[i]).strip())
    f.writelines("---------------\n")
f.close()

f = open("plus.txt", "w")
for i in indexes1:
    f.writelines(str(X_train2[i]).strip())
    f.writelines("---------------\n")
f.close()

print("Size of inliers in Train set:", train)
print("Size of inliers in Test set:", test)

train_anomaly = y_train[y_train == -1].size
test_anomaly = y_test[y_test == -1].size
print("Size of outliers in Train set:", train_anomaly)
print("Size of outliers in Test set:", test_anomaly)
