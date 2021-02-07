import json
from flask import Flask, request
from nlp.tweet_classifier import TweetClassifier


class TweetClassifierServer:
    def __init__(self):
        self.tc = TweetClassifier()
        self.tc.fit()


app = Flask(__name__)
tc_server = TweetClassifierServer()


@app.route('/')
def root():
    return 'Hello world!'


@app.route('/classify-tweet', methods=['POST'])
def classify_tweet():
    request_data = request.get_json()
    tweet = None
    prediction = None

    if request_data:
        if 'tweet' in request_data:
            tweet = request_data['tweet']
            prediction = int(tc_server.tc.predict_new(tweet)[0])

    return json.dumps({'tweet': tweet, 'prediction': prediction})


if __name__ == '__main__':
    app.run(debug=True)