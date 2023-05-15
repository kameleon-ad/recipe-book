from flask import Blueprint, jsonify
from .aspects import api as aspects_api
from .sentiments import api as sentiments_api
from .tags import api as tags_api
from .hltddbs import api as hltddbs_api

api = Blueprint('api', __name__)
api.register_blueprint(aspects_api, url_prefix='/aspects')
api.register_blueprint(sentiments_api, url_prefix='/sentiments')
api.register_blueprint(tags_api, url_prefix='/tags')
api.register_blueprint(hltddbs_api, url_prefix='/hltddbs')


@api.route('/test', methods=['GET'])
def api_test():
    return jsonify({'message': 'The api router is working'})
