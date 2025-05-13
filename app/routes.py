from flask import request, render_template, flash, redirect, url_for
from app import app, db
from app.forms import PostForm, LoginForm, RegistrationForm, EditProfileForm, EmptyForm
from flask_login import current_user, login_user, logout_user, login_required
import sqlalchemy as sa
from app.models import User, Post
from urllib.parse import urlsplit
from datetime import datetime, timezone

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Udostępniono post!')
        return redirect(url_for('index'))
    page = request.args.get('page', 1, type=int)
    posts = db.paginate(current_user.following_posts(), page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    
    next_url = url_for('index', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('index', page=posts.prev_num) \
        if posts.has_prev else None
    
    return render_template('index.html', title='Strona Glowna', 
                           form=form, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.nazwa == form.nazwa.data))
        if user is None or not user.check_password(form.haslo.data):
            flash('Niepoprawna nazwa bądź hasło!')
            return redirect(url_for('login'))
        login_user(user, remember=form.pamietaj_mnie.data)
        next_page = request.args.get('next')
        if not next_page or urlsplit(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Zarejestruj Się', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(nazwa=form.nazwa.data, email=form.nazwa.data)
        user.set_password(form.haslo.data)
        db.session.add(user)
        db.session.commit()
        flash('Gratulacje! Utworzyłeś konto!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route('/user/<nazwa>')
@login_required
def user(nazwa):
    user = db.first_or_404(sa.select(User).where(User.nazwa == nazwa))
    page = request.args.get('page', 1, type=int)
    query = user.posts.select().order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('user', nazwa=user.nazwa , page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', nazwa=user.nazwa , page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items, 
                            next_url=next_url, prev_url=prev_url, form=form)

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.ostatnio_widziany = datetime.now(timezone.utc)
        db.session.commit()

@app.route('/edytuj_profil', methods=['GET', 'POST'])
@login_required
def edytuj_profil():
    form = EditProfileForm(current_user.nazwa)
    if form.validate_on_submit():
        current_user.nazwa = form.nazwa.data
        current_user.o_mnie = form.o_mnie.data
        db.session.commit()
        flash('Zmiany zostały zapisane.')
        return redirect(url_for('edytuj_profil'))
    elif request.method == 'GET':
        form.nazwa.data == current_user.nazwa
        form.o_mnie.data = current_user.o_mnie
    return render_template('edit_profile.html', title='Edytuj Profil', form=form)

@app.route('/follow/<nazwa>', methods=['POST'])
@login_required
def follow(nazwa):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.nazwa == nazwa))
        if user is None:
            flash(f'Nie znaleziono użytkownika {nazwa}.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('Nie możesz obserwować siebie!')
            return redirect(url_for('user', nazwa=nazwa))
        current_user.follow(user)
        db.session.commit()
        flash(f'Obserwujesz {nazwa}!')
        return redirect(url_for('user', nazwa=nazwa))
    else:
        return redirect(url_for('index'))

@app.route('/unfollow/<nazwa>', methods=['POST'])
@login_required
def unfollow(nazwa):
    form = EmptyForm()
    if form.validate_on_submit():
        user = db.session.scalar(
            sa.select(User).where(User.nazwa == nazwa))
        if user is None:
            flash(f'Nie znaleziono użytkownika {nazwa}.')
            return redirect(url_for('index'))
        if user == current_user:
            flash('Nie możesz od-obserwować siebie!')
            return redirect(url_for('user', nazwa=nazwa))
        current_user.unfollow(user)
        db.session.commit()
        flash(f'Przestałeś obserwować {nazwa}!')
        return redirect(url_for('user', nazwa=nazwa))
    else:
        return redirect(url_for('index'))

@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    query = sa.select(Post).order_by(Post.timestamp.desc())
    posts = db.paginate(query, page=page,
                        per_page=app.config['POSTS_PER_PAGE'], error_out=False)
    next_url = url_for('explore', page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('explore', page=posts.prev_num) \
        if posts.has_prev else None
    
    return render_template("index.html", title='Odkrywaj', 
                           posts=posts.items, next_url=next_url, prev_url=prev_url)