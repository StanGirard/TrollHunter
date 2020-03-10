from rake_nltk import Rake

test = False

def extract(text: str):
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
    return r.get_ranked_phrases()

if test:
    file = open("text_example.txt", "r")
    print(extract(file.read()))
    file.close()