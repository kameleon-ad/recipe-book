from flask import Blueprint, request, jsonify
from app.models import Recipe
from app.utils.req_parser import new_recipe_parser

api = Blueprint('recipe', __name__)


@api.route('/test', methods=['GET'])
def recipes_test():
    return jsonify({'message': 'The recipes api is working'})


@api.route('/', methods=['GET'])
def get_all_recipes():
    return jsonify(Recipe.all())


@api.route('/', methods=['POST'])
def add_new_recipe():
    # title, ingredients, instructions for preparation, cook time and relevant tags
    data = new_recipe_parser(request.form)
    return jsonify(Recipe.add_new_recipe(**data).raw)


@api.route('/<string:recipe_pid>', methods=['GET'])
def get_recipe(recipe_pid: str):
    recipe = Recipe.get_recipe(recipe_pid)
    if recipe is None:
        return jsonify({'recipe': 'Recipe does not exist'}), 404
    return jsonify(recipe.raw)


@api.route('/<string:recipe_pid>', methods=['POST', 'PUT'])
def set_sentiment(recipe_pid: str):
    data = new_recipe_parser(request.form)
    recipe = Recipe.get_recipe(recipe_pid)
    if recipe is None:
        return jsonify({'recipe': 'Recipe does not exist'}), 404
    return jsonify(recipe.set(data).raw)
