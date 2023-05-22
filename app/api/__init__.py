from flask import Blueprint, jsonify
from .tags import api as tags_api
from .recipes import api as recipes_api

api = Blueprint('api', __name__)
api.register_blueprint(tags_api, url_prefix='/tags')
api.register_blueprint(recipes_api, url_prefix='/recipes')


@api.route('/test', methods=['GET'])
def api_test():
    return jsonify({'message': 'The api router is working'})
