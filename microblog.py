import sqlalchemy as sa
import sqlalchemy.orm as so
from app import app, db
from app.models import User, Post
from flask import Flask, render_template

app = Flask(__name__)
app.config['SECRET_KEY'] = 'you-will-never-guess'

@app.shell_context_processor
def make_shell_context():
    return {'sa': sa, 'so': so, 'db': db, 'User': User, 'Post': Post}

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Lukasz'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Nice day in Portland!'
        },
        {
            "author": {'username': 'Susan'},
            'body': 'The Avengers movie was so boring!'
        }
    ]
    return render_template('index.html', title="Home", user=user, posts=posts)