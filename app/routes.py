from flask import render_template, flash, redirect
from app import app
from app.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Ziutek'}
    posts = [
        {
            'author': {'username': 'John Lennon'},
            'body': 'Żyje.'
        },
        {
            'author': {'username': 'Saul Goodman'},
            'body': 'Witaj w moim świecie.'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Zalogowano jako {}!', 'remember_me{}'.format(form.username.data, form.remember_me.data))
        return redirect('index')
    return render_template('login.html', title='Logowanie', form=form)