from typing import Optional
import sqlalchemy as sqlalchemy
import sqlalchemy.orm as sql_orm
from app import db
from datetime import datetime,timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

followers = sqlalchemy.Table(
    'followers',
    db.metadata,
    sqlalchemy.Column('follower_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'),
              primary_key=True),
    sqlalchemy.Column('followed_id', sqlalchemy.Integer, sqlalchemy.ForeignKey('user.id'),
              primary_key=True)
)

class User(UserMixin,db.Model):
    id: sql_orm.Mapped[int] = sql_orm.mapped_column(primary_key=True)
    username: sql_orm.Mapped[str] = sql_orm.mapped_column(sqlalchemy.String(64),unique=True, index=True)
    email: sql_orm.Mapped[str] = sql_orm.mapped_column(sqlalchemy.String(120),unique=True, index=True)
    password_hash: sql_orm.Mapped[Optional[str]] = sql_orm.mapped_column(sqlalchemy.String(256))
    
    
    about_me: sql_orm.Mapped[Optional[str]] = sql_orm.mapped_column(sqlalchemy.String(140))
    last_seen: sql_orm.Mapped[Optional[datetime]] = sql_orm.mapped_column(default=lambda:datetime.now(timezone.utc))
    
    following: sql_orm.WriteOnlyMapped['User'] = sql_orm.relationship(
        secondary=followers, primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        back_populates='followers')
    followers: sql_orm.WriteOnlyMapped['User'] = sql_orm.relationship(
        secondary=followers, primaryjoin=(followers.c.followed_id == id),
        secondaryjoin=(followers.c.follower_id == id),
        back_populates='following')
    
    posts: sql_orm.WriteOnlyMapped['Post'] = sql_orm.relationship(
        back_populates='author')
    
    def __repr__(self):
        return '<User {}>'.format(self.username)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)
    
    def follow(self, user):
        if not self.is_following(user):
            self.following.add(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.following.remove(user)

    def is_following(self, user):
        query = self.following.select().where(User.id == user.id)
        return db.session.scalar(query) is not None

    def followers_count(self):
        query = sqlalchemy.select(sqlalchemy.func.count()).select_from(
            self.followers.select().subquery())
        return db.session.scalar(query)

    def following_count(self):
        query = sqlalchemy.select(sqlalchemy.func.count()).select_from(
            self.following.select().subquery())
        return db.session.scalar(query)
    
    def following_posts(self):
        Author = sql_orm.aliased(User)
        Follower = sql_orm.aliased(User)
        return (
            sqlalchemy.select(Post)
            .join(Post.author.of_type(Author))
            .join(Author.followers.of_type(Follower))
            .where(Follower.id == self.id)
            .order_by(Post.timestamp.desc())
        )
    
    
class Post(db.Model):
    id: sql_orm.Mapped[int] = sql_orm.mapped_column(primary_key=True)
    body: sql_orm.Mapped[str] = sql_orm.mapped_column(sqlalchemy.String(140))
    timestamp: sql_orm.Mapped[datetime] = sql_orm.mapped_column(default=lambda:datetime.now(timezone.utc),index=True)
    user_id: sql_orm.Mapped[int] = sql_orm.mapped_column(sqlalchemy.ForeignKey(User.id),index=True)
    
    author: sql_orm.Mapped[User] = sql_orm.relationship(back_populates='posts')
    
    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))