from app import app,db
import sqlalchemy as sqlalchemy
import sqlalchemy.orm as sql_orm
from app.models import User, Post

@app.shell_context_processor
def make_shell_context():
    return {'sqlalchemy' : sqlalchemy,'sql_orm' : sql_orm,'db': db, 'User': User, 'Post': Post}
