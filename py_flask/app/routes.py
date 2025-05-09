from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm
@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Berry Johns'}
    relatedPost = [
        {
            'author': {'username': 'John Doe'},
            'body': 'This is the first post!'
        },
        {
            'author': {'username': 'Jane Doe'},
            'body': 'This is the second post!'
        },
        {
            'author': {'username': 'Alice Smith'},
            'body': 'This is the third post!'
        }
    ]
    return render_template('index.html', title='Home', user=user, relatedPost=relatedPost)
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)