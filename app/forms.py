from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired,ValidationError,email,equal_to
from app import db
from app.models import User
import sqlalchemy as sqlalchemy

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')
    
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(),email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),equal_to('password')])
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        user = db.session.scalar(sqlalchemy.select(User).where(User.username == username.data))
        if user is not None:
            raise ValidationError('Please use a different username.')
    
    def validate_email(self, email):
        user2 = db.session.scalar(sqlalchemy.select(User).where(User.email == email.data))
        if user2 is not None:
            raise ValidationError('Please use a different email address.')
        