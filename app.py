from data_models import db, Author, Book
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)   # Create Flask app

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"

db.init_app(app)




# This is the code to generate the tables. Commented out after the first run
"""
with app.app_context():
  db.create_all()
"""
