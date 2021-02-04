"""SQLAlchemy models and utility functions for Twitoff Application"""

from flask_sqlalchemy import SQLAlchemy


DB = SQLAlchemy()


# User table
class User(DB.Model):
    """Twitter User Table that will correspond to tweets - SQLAlchemy syntax"""

    id = DB.Column(DB.BigInteger, primary_key=True)  # id column (primary key)
    name = DB.Column(DB.String, nullable=False)  # name column

    def __repr__(self):
        return "<User: {}>".format(self.name)


# Twitter table
class Tweet(DB.Model):
    """Tweet text data - associated with Users Table"""

    id = DB.Column(DB.BigInteger, primary_key=True)  # id column (primary key)
    text = DB.Column(DB.Unicode(300))
    user_id = DB.Column(DB.BigInteger, DB.ForeignKey("user.id"), nullable=False)
    user = DB.relationship("User", backref=DB.backref("tweets", lazy=True))

    def __repr__(self):
        return "<Tweet: {}>".format(self.text)


def insert_example_users():

    henry = User(id=1, name="hcmead")
    paula = User(id=2, name="PaulaAndreaMead")
    DB.session.add(henry)
    DB.session.add(paula)
    DB.session.commit()
