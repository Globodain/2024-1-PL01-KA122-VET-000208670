from datetime import datetime, timezone
from typing import Optional
import sqlalchemy as sa # elements for editing database
import sqlalchemy.orm as so # elements for database structure
from app import db

class User(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key = True)
  username: so.Mapped[str] = so.mapped_column(sa.String(64), index=True, unique = True)
  email: so.Mapped[str] = so.mapped_column(sa.String(120), index=True, unique = True)
  password_hash: so.Mapped[Optional[str]] = so.mapped_column(sa.String(256))
  posts: so.WriteOnlyMapped['Post'] = so.relationship(back_populates='author')
  # so.mapped_column() - adds additional properties to columns
  # Optional[] - allows column to be empty or nullable

  # tells Python how to print object like toString() in Java
  def __repr__(self):
    return '<User {}>'.format(self.username)
  
class Post(db.Model):
  id: so.Mapped[int] = so.mapped_column(primary_key=True)
  body: so.Mapped[str] = so.mapped_column(sa.String(140))
  timestamp: so.Mapped[datetime] = so.mapped_column(index=True, default=lambda: datetime.now(timezone.utc))
  user_id: so.Mapped[int] = so.mapped_column(sa.ForeignKey(User.id), index=True)
  author: so.Mapped[User] = so.relationship(back_populates='posts')

  def __repr__(self):
    return '<Post {}>'.format(self.body)