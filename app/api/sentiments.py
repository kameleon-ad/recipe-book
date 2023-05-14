from flask import Blueprint, request, jsonify
from app.models import Sentiment as SentimentModel

api = Blueprint('sentiments', __name__)


@api.route('/test', methods=['GET'])
def sentiment_test():
    return jsonify({'message': 'The sentiments api is working'})


@api.route('/', methods=['GET'])
def get_all_sentiments():
    return jsonify([sentiment.raw for sentiment in SentimentModel.get_all_sentiments()])


@api.route('/', methods=['POST'])
def add_new_sentiment():
    sentiment = request.form['sentiment']
    return jsonify(SentimentModel.add_new_sentiment(sentiment).raw)
