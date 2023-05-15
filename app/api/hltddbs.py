from flask import Blueprint, request, jsonify, Response, current_app
import asyncio
from app.models import Hltddb
from app.utils.fileOps import to_csv, from_csv, store_db

api = Blueprint('hltddb', __name__)


@api.route('/test', methods=['GET'])
def hltddbs_test():
    return jsonify({'message': 'The hltddbs api is working'})


@api.route('/', methods=['GET'])
def get_all_hltddbs():
    return jsonify(Hltddb.all())


@api.route('/', methods=['POST'])
def add_new_hltddb():
    text = request.form['text']
    return jsonify(Hltddb.add_new_hltddb(text).raw)


@api.route('/hltddb/<string:hltddb_pid>', methods=['GET'])
def get_hltddb(hltddb_pid: str):
    hltddb = Hltddb.get_hltddb(hltddb_pid)
    if hltddb is None:
        return jsonify({'hltddb': 'Hltddb does not exist'}), 404
    return jsonify(hltddb.raw)


@api.route('/hltddb/<string:hltddb_pid>/<string:aspect_pid>', methods=['GET'])
def get_sentiment(hltddb_pid: str, aspect_pid: str):
    hltddb = Hltddb.get_hltddb(hltddb_pid)
    if hltddb is None:
        return jsonify({'hltddb': 'Hltddb does not exist'}), 404
    sentiment = hltddb.get_sentiment(aspect_pid)
    if sentiment is None:
        return jsonify({'sentiment': 'Sentiment is not defined'}), 404
    return jsonify(sentiment.raw)


@api.route('/hltddb/<string:hltddb_pid>/<string:aspect_pid>', methods=['POST', 'PUT'])
def set_sentiment(hltddb_pid: str, aspect_pid: str):
    hltddb = Hltddb.get_hltddb(hltddb_pid)
    if hltddb is None:
        return jsonify({'hltddb': 'Hltddb does not exist'}), 404
    sentiment_pid = request.form['sentiment']
    sentiment = hltddb.set_sentiment(aspect_pid, sentiment_pid).raw
    return jsonify(sentiment)


@api.route('/file', methods=['GET'])
async def download_file():
    whole_data = Hltddb.all()

    if len(whole_data) == 0:
        return jsonify({'message': 'There is no data'}), 404

    event_loop = asyncio.get_event_loop()
    csv_file = await event_loop.run_in_executor(None, to_csv, whole_data)

    filename = 'data.csv'
    response = Response(csv_file, mimetype='text/csv')
    response.headers.set('Content-Disposition', 'attachment', filename=filename)
    return response


@api.route('/file', methods=['POST'])
async def upload_file():
    if 'csv_file' not in request.files:
        return jsonify({'message': 'No file provided'}), 400

    csv_file = request.files['csv_file']
    event_loop = asyncio.get_event_loop()
    csv_data = await event_loop.run_in_executor(None, from_csv, csv_file)

    cnt = await event_loop.run_in_executor(None, store_db, csv_data)

    return {'total': cnt}
