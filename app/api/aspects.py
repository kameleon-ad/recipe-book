from flask import Blueprint, request, jsonify
from app.models import Aspect as AspectModel

api = Blueprint('aspects', __name__)


@api.route('/test', methods=['GET'])
def aspects_test():
    return jsonify({'message': 'The aspects api is working'})


@api.route('/', methods=['GET'])
def get_all_aspects():
    return jsonify([aspect.raw for aspect in AspectModel.get_all_aspects()])


@api.route('/', methods=['POST'])
def add_new_aspect():
    aspect = request.form['aspect']
    return jsonify(AspectModel.add_new_aspect(aspect).raw)
