import os
import json
import random

from flask_seeder import Seeder

from app.extensions import db
from app.models import Aspect, Sentiment, Tag, HltddbTag, Hltddb


class OpinionAiSeeder(Seeder):
    config: dict

    def run(self):
        with open(os.getenv('DB_SEED_CFG'), "r") as fp:
            self.config = json.load(fp)

        for model in reversed([Aspect, Sentiment, Tag, Hltddb, HltddbTag]):
            model.query.delete()

        aspects = [Aspect(aspect=aspect) for aspect in self.config['aspects']]
        sentiments = [Sentiment(sentiment=sentiment) for sentiment in self.config['sentiments']]

        for aspect in aspects:
            db.session.add(aspect)

        for sentiment in sentiments:
            db.session.add(sentiment)

        db.session.commit()

        for _ in range(self.config['size_tags']):
            aspect = random.choice(aspects)
            sentiment = random.choice(sentiments)
            tag = Tag(aspect_pid=aspect.pid, sentiment_pid=sentiment.pid)
            db.session.add(tag)

        db.session.commit()

        hltddbs = [Hltddb(text=text) for text in self.config['texts']]
        for hltddb in hltddbs:
            db.session.add(hltddb)

        db.session.commit()

        for _ in range(self.config['size_hltddbs_tags']):
            aspect = random.choice(aspects)
            sentiment = random.choice(sentiments)
            hltddb = random.choice(hltddbs)
            hltddb.set_sentiment(aspect.pid, sentiment.pid)

        db.session.commit()
