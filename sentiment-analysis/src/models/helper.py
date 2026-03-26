from sklearn.feature_extraction.text import TfidfVectorizer
import re
import string


def clean_text(text):
    text = text.lower()

    text = re.sub(r"<.*?>", "", text)

    text = text.translate(str.maketrans("", "", string.punctuation))

    text = re.sub(r"\d+", "", text)
    return text


tfidf = TfidfVectorizer(
    max_features=5000,
    stop_words="english"
)
