"""Main app/routing file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User


# creates application
def create_app():
    """Creating and configuring an instance of the Flask application"""
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///db.sqlite3"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    DB.init_app(app)

    @app.route('/')
    def root():
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', title="home", users=User.query.all())

    return app
