from app import db
import sqlalchemy as sa
import sqlalchemy.orm as orm
from typing import Optional

class User(db.Model):
  id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
  username: orm.Mapped[str] = orm.mapped_column(sa.String(64), unique=True, index=True)
  email: orm.Mapped[str] = orm.mapped_column(sa.String(120), unique=True, index=True)
  password_hash: orm.Mapped[Optional[str]] = orm.mapped_column(sa.String(256))
  posts: orm.WriteOnlyMapped['Post'] = orm.relationship(back_populates='author')
  
  def __repr__(self) -> str:
    return f"<User {self.username}>"
  
class Post(db.Model):
  id: orm.Mapped[int] = orm.mapped_column(primary_key=True)
  body: orm.Mapped[str] = orm.mapped_column(sa.String(140))
  timestamp: orm.Mapped[sa.DateTime] = orm.mapped_column(sa.DateTime, server_default=sa.func.now(), index=True)
  user_id: orm.Mapped[int] = orm.mapped_column(sa.ForeignKey(User.id), index=True)
  author: orm.Mapped[User] = orm.relationship(back_populates="posts")     

