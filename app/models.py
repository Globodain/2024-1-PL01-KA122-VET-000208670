from typing import Optional
import sqlalchemy as sqlalchemy
import sqlalchemy.orm as sql_orm
from app import db
from datetime import datetime,timezone
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5

class User(UserMixin,db.Model):
    id: sql_orm.Mapped[int] = sql_orm.mapped_column(primary_key=True)
    username: sql_orm.Mapped[str] = sql_orm.mapped_column(sqlalchemy.String(64),unique=True, index=True)
    email: sql_orm.Mapped[str] = sql_orm.mapped_column(sqlalchemy.String(120),unique=True, index=True)
    password_hash: sql_orm.Mapped[Optional[str]] = sql_orm.mapped_column(sqlalchemy.String(256))
    
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