"""
Use flask ORM to build tweet objects/events and store them into postgres
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_

from datetime import datetime, timedelta

# Set up database -- first check if you forgot your environment variables
# need to create pointer named db

db_string = "postgres://rrxfutkudyqfwo:4e3e8e27b8eb4c1f73e90c5cf6e3f2c4f3a1da373a3cd839b864cdf54a90b89b@ec2-52-71-85-210.compute-1.amazonaws.com:5432/du11chbkt78no"

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


if __name__== '__main__':

    with app.app_context():
        #db.create_all()
        #tweets = Tweet.query.all()
        for t in tweets:
            print(f"{t.zipcode} at {t.timestamp} said: {t.text}")
