from app import db, login
import sqlalchemy as sa
import sqlalchemy.orm as orm
from typing import Optional
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import sha256

class User(UserMixin, db.Model):
  id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
  username: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
  email: orm.Mapped[str] = orm.mapped_column(sa.String(120), unique=True, index=True)
  password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(256))
  posts: orm.WriteOnlyMapped['Post'] = orm.relationship(back_populates='author')

  def set_password(self, password):
      self.password_hash = generate_password_hash(password)

  def check_password(self, password):
      return check_password_hash(self.password_hash, password)

  def __repr__(self) -> str:
    return f"<User {self.username}>"
    
  def avatar(self, size):
    return f"https://www.gravatar.com/avatar/{sha256(self.email.encode('utf-8')).hexdigest()}?d=identicon&s={size}"

  
class Post(db.Model):
  id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
  body: orm.Mapped[str] = orm.mapped_column(sa.String(140))
  timestamp: orm.Mapped[sa.DateTime] = orm.mapped_column(sa.DateTime, server_default=sa.func.now(), index=True)
  user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(User.id), index=True)
  author: orm.Mapped[User] = orm.relationship(back_populates="posts")

  def __repr__(self) -> str:
    return f"<Post {self.id}>"


@login.user_loader
def load_user(id):
    return db.session.get(User, int(id))