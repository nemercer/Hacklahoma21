import pandas as pd
import spacy
import string
import dill
import os.path
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from spacy.lang.en.stop_words import STOP_WORDS
from spacy.lang.en import English

from nlp.preprocess_data import load_df


class TweetClassifier:
    def __init__(self):
        self.df = load_df()
        # self.df['num_words_text'] = self.df['tweet'].apply(lambda x: len(str(x).split()))
        # mask = self.df['num_words_text'] > 2
        # self.df = self.df[mask]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(self.df['tweet'], self.df['class'], test_size=0.2, random_state=42)

        self.nlp = spacy.load('en_core_web_sm')
        self.punctiations = string.punctuation
        self.stop_words = STOP_WORDS
        self.parser = English()

        self.bow_vector = CountVectorizer(tokenizer=self.tokenizer, ngram_range=(1, 1))
        self.tfidf_vector = TfidfVectorizer(tokenizer=self.tokenizer)

        self.pipe = None

    def tokenizer(self, tweet):
        tokens = self.nlp(tweet)

        # Lemmatizing.
        tokens = [word.lemma_ if word.lemma_ != "-PRON-" else word.lower_ for word in tokens]

        # Remove stop words.
        tokens = [word for word in tokens if word not in self.stop_words and word not in self.punctiations]

        return tokens

    def fit(self):
        lr_classifier = LogisticRegression(max_iter=5000)
        self.pipe = Pipeline([('cleaner', Cleaner()),
                         ('vectorizer', self.bow_vector),
                         ('classifier', lr_classifier)])

        self.pipe.fit(self.X_train, self.y_train)

    def predict(self):
        predictions = self.pipe.predict(self.X_test)
        print("Logistic Regression Accuracy:", metrics.accuracy_score(self.y_test, predictions))

    def predict_new(self, new_tweet):
        prediction = self.pipe.predict([new_tweet])

        print(new_tweet, prediction)


class Cleaner(TransformerMixin):
    """ Custom transformer using SpaCy.
    """
    def transform(self, X, **transform_params):
        return [self.clean(tweet) for tweet in X]

    def fit(self, X, y=None, **fit_params):
        return self

    def get_params(self, deep=True):
        return {}

    def clean(self, tweet):
        return tweet.strip().lower()


if __name__ == '__main__':
    tc = TweetClassifier()
    tc.fit()
    tc.predict()