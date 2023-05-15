import asyncio
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import json
from threading import Thread

from app.extensions import db, instances
from app.models import Hltddb


def to_csv(raw_data):

    def json_processor(row):
        return json.dumps(row.tags)

    tmp_df = pd.DataFrame(raw_data)
    tmp_df['tags'] = tmp_df.apply(json_processor, axis=1)
    return tmp_df.to_csv(index=False)


def from_csv(csv_data):
    return pd.read_csv(csv_data)


async def distributed_store_db(csv_file):
    executor = ProcessPoolExecutor()
    store_db_tasks = []
    cnt = 0
    app = instances['app']

    for chunk in pd.read_csv(csv_file, chunksize=10000):
        thread = Thread(target=store_db, args=(chunk, app))
        thread.start()
        # event_loop = asyncio.get_event_loop()
        # task = event_loop.run_in_executor(executor, store_db, chunk, app)
        # task = executor.submit(store_db, chunk, app)
        store_db_tasks.append(thread)

    for thread in store_db_tasks:
        thread.join()
    return len(store_db_tasks)


def store_db(df: pd.DataFrame, app=None):
    cnt = 0
    db_instances = []
    if app is None:
        app = instances['app']
    Session = instances['session_maker']
    session = Session(twophase=True)

    def feature_extractor(item):
        return {"text": item.text}

    for _, row in df.iterrows():
        db_instances.append(Hltddb(**feature_extractor(row)))
        cnt += 1

    with session.begin():
        with app.app_context():
            # session.bulk_insert_mappings(Hltddb, db_instances)
            session.bulk_save_objects(db_instances)
    return cnt
