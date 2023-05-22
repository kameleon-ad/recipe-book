import os
import json
import random

from flask_seeder import Seeder

from app.extensions import db
from app.models import Aspect, Sentiment, Tag, RecipeTag, Recipe


class OpinionAiSeeder(Seeder):
    config: dict

    def run(self):
        with open(os.getenv('DB_SEED_CFG'), "r") as fp:
            self.config = json.load(fp)

        for model in reversed([Aspect, Sentiment, Tag, Recipe, RecipeTag]):
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

        recipes = [Recipe(text=text) for text in self.config['texts']]
        for recipe in recipes:
            db.session.add(recipe)

        db.session.commit()

        for _ in range(self.config['size_recipes_tags']):
            aspect = random.choice(aspects)
            sentiment = random.choice(sentiments)
            recipe = random.choice(recipes)
            recipe.set_sentiment(aspect.pid, sentiment.pid)

        db.session.commit()
