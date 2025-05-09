from flask import render_template, flash, redirect, url_for
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username':'Miguel'}
    posts = [
        {
            'author':{'username':'John'},
            'body' : 'First post!'
        },
        {
            'author':{'username':'Susan'},
            'body' : 'Second post!'
        }
    ]
    return render_template('index.html', user=user, posts = posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested from user {}, rember_me={}'.format(
            form.username.data, form.remember_me.data
        ))
        return redirect(url_for('index'))
    return render_template('login.html', title="Sign In", form=form)