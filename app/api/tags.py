from flask import Blueprint, request, jsonify
from app.models import Tag as TagModel

api = Blueprint('tags', __name__)


@api.route('/test', methods=['GET'])
def tags_test():
    return jsonify({'message': 'The tags api is working'})


@api.route('/', methods=['GET'])
def get_all_tags():
    return jsonify([tag.raw for tag in TagModel.get_all_tags()])


@api.route('/', methods=['POST'])
def insert_tag():
    aspect_pid = request.form['aspect']
    sentiment_pid = request.form['sentiment']
    return jsonify(TagModel.insert_tag(aspect_pid, sentiment_pid).raw)
