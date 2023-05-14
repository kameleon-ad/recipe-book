from flask import Blueprint, jsonify

api = Blueprint('api', __name__)


@api.route('/test', methods=['GET'])
def api_test():
    return jsonify({'message': 'The api router is working'})
