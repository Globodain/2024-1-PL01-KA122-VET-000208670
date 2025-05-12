from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User
from wtforms import TextAreaField
from wtforms.validators import Length

class LoginForm(FlaskForm):
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    pamietaj_mnie = BooleanField('Pamiętaj Mnie')
    submit = SubmitField('Zarejestruj Się')

class RegistrationForm(FlaskForm):
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    haslo2 = PasswordField(
        'Powtórz hasło', 
        validators=[DataRequired(),
        EqualTo('haslo')])
    submit = SubmitField('Zarejestruj')

    def walidacja_nazwy(self, nazwa):
        user = db.session.scalar(sa.select(User).where(
            User.nazwa == nazwa.data))
        
        if user is not None:
            raise ValidationError('Nazwa jest zajęta!')
        
    def walidacja_emaila(self, email):
        user = db.session.scalar(sa.select(User).where(
            User.email == email.data))
        
        if user is not None:
            raise ValidationError('Użyj innego adresu email!')
        
class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = db.session.scalar(sa.select(User).where(
                User.username == username.data))
            if user is not None:
                raise ValidationError('Please use a different username.')