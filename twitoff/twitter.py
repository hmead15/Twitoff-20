"""
Retireve Tweets, embeddings, and persist in database
"""
from os import getenv
import tweepy
import spacy
from .models import DB, Tweet, User

TWITTER_USERS = ["hcmead", "Paula Andrea Mead", "nasa", "rrherr"]

TWITTER_API_KEY = getenv("TWITTER_API_KEY")
TWITTER_API_SECRET_KEY = getenv("TWITTER_API_SECRET_KEY")

TWITTER_AUTH = tweepy.OAuthHandler(TWITTER_API_KEY, TWITTER_API_SECRET_KEY)

TWITTER = tweepy.API(TWITTER_AUTH)

nlp = spacy.load("my_model")


def vectorize_tweet(tweet_text):
    return nlp(tweet_text).vector


def add_or_update_user(username):
    """Add or update a user and their tweets, error if not a Twitter user."""
    try:
        twitter_user = TWITTER.get_user(username)
        db_user = User.query.get(twitter_user.id) or User(
            id=twitter_user.id, name=username
        )
        # Check and see if a user exists,
        #       If so, get associate db_user with that twitter_user's id
        #       If not, create a new User
        DB.session.add(db_user)
        # Let's get the tweets
        tweets = twitter_user.timeline(
            count=200, exclude_replies=True, include_rts=False, tweet_mode="Extended"
        )
        # Add tweets to DB
        for tweet in tweets:
            vectorized_tweet = vectorize_tweet(tweet.full_text)
            db_tweet = Tweet(
                id=tweet.id, text=tweet.full_text[:300], vect=vectorized_tweet
            )
            db_user.tweet.append(db_tweet)
    except Exception as e:
        print("Error processing {}: {}".format(username, e))
        raise e
    else:
        DB.session.commit()