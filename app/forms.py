from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField,TextAreaField
from wtforms.validators import DataRequired,ValidationError,email,equal_to,length
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
        
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[length(min=0,max=140)])
    submit = SubmitField('Submit')
    
    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username
        
    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sqlalchemy.select(User).where(User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')
            
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')