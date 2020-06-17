"""
Use ORM to build tweet objects/events, and store them in postgres
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from datetime import datetime, timedelta

# Set up database -- first check if you forgot your environment variables
# need to create pointer named db

db_string = "postgres://rrxfutkudyqfwo:4e3e8e27b8eb4c1f73e90c5cf6e3f2c4f3a1da373a3cd839b864cdf54a90b89b@ec2-52-71-85-210.compute-1.amazonaws.com:5432/du11chbkt78no"

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = db_string
db = SQLAlchemy(app)


class Example(db.Model):
    __tablename__ = 'examples'
    id = db.Column(db.Integer,primary_key=True)
    zipcode = db.Column(db.String,nullable=False)
    text = db.Column(db.String)
    t1 = db.Column(db.DateTime, nullable=False)
    t2 = db.Column(db.DateTime, default=t1-timedelta(hours=1))

    def fill_text(self):
        # query by time and zipcode
        tweets = Tweet.query.all()
        for t in tweets:
            self.text.append(t.text)
            #session.delete(t) # optionally delete exampled tweets to


class Tweet(db.Model):
    # this table offers temporary storage for individual tweets
    __tablename__ = 'tweets'
    id = db.Column(db.Integer,primary_key=True)
    zipcode = db.Column(db.String,nullable=False)
    text = db.Column(db.String,nullable=False)
    timestamp = db.Column(db.DateTime, default=datetime.now)

    def add_self(self):
        db.session.add(self)
        db.session.commit()


@app.route("/")
def index():
    """
    Index page to stream
    """
    return "<h1> hello world! </h1>"



if __name__== '__main__':
    with app.app_context():
        tweets = Tweet.query.all()
        for t in tweets:
            print(f"{t.zipcode} at {t.timestamp} said: {t.text}")
    #db.create_all()
