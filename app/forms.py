from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
import sqlalchemy as sa
from app import db
from app.models import User

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