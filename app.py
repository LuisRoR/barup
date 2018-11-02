from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import enum

from flask import Markup
from flask import render_template

app = Flask(__name__)
app.config['DEBUG'] = True      # displays runtime errors in the browser, too
# TESTING BARUP app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost/blogz'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://postgres@localhost/barup'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#app.config['POSTS_PER_PAGE'] = 3
db = SQLAlchemy(app)
app.secret_key = b'\xed\xd5G\xb8l\xd7J\x02\x83_\xe2\x1f\xf5<\xeaM'