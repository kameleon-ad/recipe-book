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


def store_db(df: pd.DataFrame, *_args):
    cnt = 0
    db_instances = []
    app = instances['app']

    for _, row in df.iterrows():
        db_instances.append(Hltddb(text=row.text))
        cnt += 1

    with app.app_context():
        db.session.bulk_save_objects(db_instances)
        db.session.commit()
    return cnt
