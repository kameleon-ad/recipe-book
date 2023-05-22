from flask import Blueprint, request, jsonify, Response
from app.models import Recipe

api = Blueprint('recipe', __name__)


@api.route('/test', methods=['GET'])
def recipes_test():
    return jsonify({'message': 'The recipes api is working'})


@api.route('/', methods=['GET'])
def get_all_recipes():
    return jsonify(Recipe.all())


@api.route('/', methods=['POST'])
def add_new_recipe():
    text = request.form['text']
    return jsonify(Recipe.add_new_recipe(text).raw)


@api.route('/recipe/<string:recipe_pid>', methods=['GET'])
def get_recipe(recipe_pid: str):
    recipe = Recipe.get_recipe(recipe_pid)
    if recipe is None:
        return jsonify({'recipe': 'Recipe does not exist'}), 404
    return jsonify(recipe.raw)


@api.route('/recipe/<string:recipe_pid>/<string:aspect_pid>', methods=['GET'])
def get_sentiment(recipe_pid: str, aspect_pid: str):
    recipe = Recipe.get_recipe(recipe_pid)
    if recipe is None:
        return jsonify({'recipe': 'Recipe does not exist'}), 404
    sentiment = recipe.get_sentiment(aspect_pid)
    if sentiment is None:
        return jsonify({'sentiment': 'Sentiment is not defined'}), 404
    return jsonify(sentiment.raw)


@api.route('/recipe/<string:recipe_pid>/<string:aspect_pid>', methods=['POST', 'PUT'])
def set_sentiment(recipe_pid: str, aspect_pid: str):
    recipe = Recipe.get_recipe(recipe_pid)
    if recipe is None:
        return jsonify({'recipe': 'Recipe does not exist'}), 404
    sentiment_pid = request.form['sentiment']
    sentiment = recipe.set_sentiment(aspect_pid, sentiment_pid).raw
    return jsonify(sentiment)
