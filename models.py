"""
Use flask ORM to build tweet objects/events and store them into postgres
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_
from dotenv import load_dotenv

from datetime import datetime, timedelta
import os

load_dotenv()
# need to create pointer named db
db_string = os.getenv("DB_STRING")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Example(db.Model):
    __tablename__ = 'examples'
    id = db.Column(db.Integer,primary_key=True)
    zipcode = db.Column(db.String,nullable=False)
    text = db.Column(db.String)
    t1 = db.Column(db.DateTime, nullable=False)
    t2 = db.Column(db.DateTime, nullable=False) # some time ago

    def fill_text(self):
        # query by time and zipcode
        tweets = Tweet.query.filter(and_(Tweet.timestamp >= self.t2, Tweet.timestamp < self.t1,Tweet.zipcode == self.zipcode)).all()
        total = ''
        for t in tweets:
            total += t.text
            #session.delete(t) # optionally delete example-ingested tweets to save row space
        self.text = total
        db.session.commit()

    def create_json(self):
        d = {"props":{},"contents":{}}
        for emoji in self.text:
            d["contents"][emoji] = d["contents"].get(emoji, 0) + 1
        d["props"]["zip"] = self.zipcode
        return d


    def create_json_with_weather(self):
        # this method queries for his friend in the weather table
        d = {"props":{},"contents":{},"weather":{}}
        for emoji in self.text:
            d["contents"][emoji] = d["contents"].get(emoji, 0) + 1
        d["props"]["zip"] = self.zipcode
        try:
            w = Weather.query.filter_by(recorded_at=self.t1).first()
            d["weather"] = {"description":w.description,"temperature":w.temperature}
        except AttributeError:
            d["weather"] = {"description":"oops, no entry","temperature":67}
            # currently just adding a fake temperature,, but I should manage the issue when I don't get a timestamp match...
        return d


class Tweet(db.Model):
    # this table offers temporary storage for individual tweets
    __tablename__ = 'tweets'
    id = db.Column(db.Integer,primary_key=True)
    zipcode = db.Column(db.String,nullable=False)
    text = db.Column(db.String,nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)
    # recorded_at

    def add_self(self):
        db.session.add(self)
        db.session.commit()

    def print_self(self):
        return self.text


class Weather(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer,primary_key=True)
    zipcode = db.Column(db.String,nullable=False)
    description = db.Column(db.String,nullable=False)
    temperature = db.Column(db.Float,nullable=False)
    recorded_at = db.Column(db.DateTime, default=datetime.now)


class Log(db.Model):
    __tablename__ = 'weather'
    id = db.Column(db.Integer,primary_key=True)
    error_code = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def add_self(self):
        db.session.add(self)
        db.session.commit()




if __name__== '__main__':
    # note: you can run this test code to print every example.

    with app.app_context():
        #db.create_all()

        #tweets = Tweet.query.all()
        examples = Example.query.all()

        for i in examples:
            #i.fill_text()
            p = i.create_json_with_weather()
            print(p)
        """
        for t in tweets:
            print(f"{t.zipcode} at {t.timestamp} said: {t.text}")
        """
