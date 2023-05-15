import asyncio
from concurrent.futures import ProcessPoolExecutor
import pandas as pd
import json

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
    for chunk in pd.read_csv(csv_file, chunksize=300000):
        event_loop = asyncio.get_event_loop()
        task = event_loop.run_in_executor(executor, store_db, chunk)
        store_db_tasks.append(task)
    completed, _ = await asyncio.wait(store_db_tasks)
    return cnt


def store_db(df: pd.DataFrame):
    cnt = 0
    db_instances = []
    app = instances['app']

    def feature_extractor(item):
        return {"text": item.text}

    for _, row in df.iterrows():
        db_instances.append(feature_extractor(row))
        cnt += 1

    with app.app_context():
        db.session.bulk_insert_mappings(Hltddb, db_instances)
        db.session.commit()
    return cnt
