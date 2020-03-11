from rake_nltk import Rake
import numpy as np
import math
import nltk
from nltk import word_tokenize
import string
from nltk.stem import WordNetLemmatizer

test = True

def extract(text: str):
    return extract_v2(text).union(extract_v1(text))


def extract_v1(txt: str) -> set:
    # Uses stopwords for english from NLTK, and all puntuation characters by
    # default
    r = Rake()
    # Extraction given the text
    r.extract_keywords_from_text(text)

    # Extraction given the list of strings where each string is a sentence.
    # sentences = nltk.tokenize.sent_tokenize(text)
    # r.extract_keywords_from_sentences(sentences)

    # To get keyword phrases ranked highest to lowest.
    # print(r.get_ranked_phrases())

    # To get keyword phrases ranked highest to lowest with scores.
    # print(r.get_ranked_phrases_with_scores())
    res = r.get_ranked_phrases()

    return set(res[:(10 if len(res) >= 10 else len(res))])

def extract_v2(txt: str) -> set:
    # algorithm from https://github.com/JRC1995/TextRank-Keyword-Extraction/blob/master/TextRank.ipynb

    # nltk.download('punkt')

    def clean(text):
        text = text.lower()
        printable = set(string.printable)
        text = filter(lambda x: x in printable, text)
        text = "".join(list(text))
        return text

    Cleaned_text = clean(txt)
    # print(Cleaned_text)
    text = word_tokenize(Cleaned_text)

    #print("Tokenized Text: \n")
    #print(text)

    nltk.download('averaged_perceptron_tagger')

    POS_tag = nltk.pos_tag(text)

    #print("Tokenized Text with POS tags: \n")
    #print(POS_tag)

    nltk.download('wordnet')

    wordnet_lemmatizer = WordNetLemmatizer()

    adjective_tags = ['JJ', 'JJR', 'JJS']

    lemmatized_text = []

    for word in POS_tag:
        if word[1] in adjective_tags:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0], pos="a")))
        else:
            lemmatized_text.append(str(wordnet_lemmatizer.lemmatize(word[0])))  # default POS = noun

    #print("Text tokens after lemmatization of adjectives and nouns: \n")
    #print(lemmatized_text)

    POS_tag = nltk.pos_tag(lemmatized_text)

    #print("Lemmatized text with POS tags: \n")
    #print(POS_tag)

    stopwords = []

    wanted_POS = ['NN', 'NNS', 'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'VBG', 'FW']

    for word in POS_tag:
        if word[1] not in wanted_POS:
            stopwords.append(word[0])

    punctuations = list(str(string.punctuation))

    stopwords = stopwords + punctuations
    stopword_file = open("stopwords.txt", "r")
    # Source = https://www.ranks.nl/stopwords

    lots_of_stopwords = []

    for line in stopword_file.readlines():
        lots_of_stopwords.append(str(line.strip()))

    stopwords_plus = stopwords + lots_of_stopwords
    stopwords_plus = set(stopwords_plus)
    processed_text = []
    for word in lemmatized_text:
        if word not in stopwords_plus:
            processed_text.append(word)
    #print(processed_text)
    vocabulary = list(set(processed_text))
    #print(vocabulary)

    vocab_len = len(vocabulary)

    weighted_edge = np.zeros((vocab_len, vocab_len), dtype=np.float32)

    score = np.zeros((vocab_len), dtype=np.float32)
    window_size = 3
    covered_coocurrences = []

    for i in range(0, vocab_len):
        score[i] = 1
        for j in range(0, vocab_len):
            if j == i:
                weighted_edge[i][j] = 0
            else:
                for window_start in range(0, (len(processed_text) - window_size)):

                    window_end = window_start + window_size

                    window = processed_text[window_start:window_end]

                    if (vocabulary[i] in window) and (vocabulary[j] in window):

                        index_of_i = window_start + window.index(vocabulary[i])
                        index_of_j = window_start + window.index(vocabulary[j])

                        # index_of_x is the absolute position of the xth term in the window
                        # (counting from 0)
                        # in the processed_text

                        if [index_of_i, index_of_j] not in covered_coocurrences:
                            weighted_edge[i][j] += 1 / math.fabs(index_of_i - index_of_j)
                            covered_coocurrences.append([index_of_i, index_of_j])

    inout = np.zeros((vocab_len), dtype=np.float32)

    for i in range(0, vocab_len):
        for j in range(0, vocab_len):
            inout[i] += weighted_edge[i][j]

    MAX_ITERATIONS = 50
    d = 0.85
    threshold = 0.0001  # convergence threshold

    for iter in range(0, MAX_ITERATIONS):
        prev_score = np.copy(score)

        for i in range(0, vocab_len):

            summation = 0
            for j in range(0, vocab_len):
                if weighted_edge[i][j] != 0:
                    summation += (weighted_edge[i][j] / inout[j]) * score[j]

            score[i] = (1 - d) + d * (summation)

        if np.sum(np.fabs(prev_score - score)) <= threshold:  # convergence condition
            #print("Converging at iteration " + str(iter) + "....")
            break

    #for i in range(0, vocab_len):
    #   print("Score of " + vocabulary[i] + ": " + str(score[i]))

    phrases = []

    phrase = " "
    for word in lemmatized_text:

        if word in stopwords_plus:
            if phrase != " ":
                phrases.append(str(phrase).strip().split())
            phrase = " "
        elif word not in stopwords_plus:
            phrase += str(word)
            phrase += " "

    #print("Partitioned Phrases (Candidate Keyphrases): \n")
    #print(phrases)

    unique_phrases = []

    for phrase in phrases:
        if phrase not in unique_phrases:
            unique_phrases.append(phrase)

    #print("Unique Phrases (Candidate Keyphrases): \n")
    #print(unique_phrases)

    for word in vocabulary:
        # print word
        for phrase in unique_phrases:
            if (word in phrase) and ([word] in unique_phrases) and (len(phrase) > 1):
                # if len(phrase)>1 then the current phrase is multi-worded.
                # if the word in vocabulary is present in unique_phrases as a single-word-phrase
                # and at the same time present as a word within a multi-worded phrase,
                # then I will remove the single-word-phrase from the list.
                unique_phrases.remove([word])

    #print("Thinned Unique Phrases (Candidate Keyphrases): \n")
    #print(unique_phrases)

    phrase_scores = []
    keywords = []
    for phrase in unique_phrases:
        phrase_score = 0
        keyword = ''
        for word in phrase:
            keyword += str(word)
            keyword += " "
            phrase_score += score[vocabulary.index(word)]
        phrase_scores.append(phrase_score)
        keywords.append(keyword.strip())

    i = 0
    for keyword in keywords:
        # print("Keyword: '" + str(keyword) + "', Score: " + str(phrase_scores[i]))
        i += 1

    sorted_index = np.flip(np.argsort(phrase_scores), 0)

    keywords_num = 10 if len(keywords) >= 10 else len(keywords)

    # print("Keywords:\n")

    res = []
    for i in range(0, keywords_num):
        res.append(str(keywords[sorted_index[i]]))

    return set(res)


if test:
    file = open("text_example.txt", "r")
    text = file.read()
    print(extract(text))
    file.close()