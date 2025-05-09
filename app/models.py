from typing import Optional
import sqlalchemy as sqlalchemy
import sqlalchemy.orm as sql_orm
from app import db

class User(db.Model):
    id: sql_orm.Mapped[int] = sql_orm.mapped_column(primary_key=True)
    username: sql_orm.Mapped[str] = sql_orm.mapped_column(sqlalchemy.String(64),unique=True, index=True)
    email: sql_orm.Mapped[str] = sql_orm.mapped_column(sqlalchemy.String(64),unique=True, index=True)
    password_hash: sql_orm.Mapped[Optional[str]] = sql_orm.mapped_column(nullable=False)
    
    def __repr__(self):
        return '<User {}>'.format(self.username)