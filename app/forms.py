from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length
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

class EditProfileForm(FlaskForm):
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    o_mnie = TextAreaField('O mnie', validators=[Length(min=0, max=140)])
    submit = SubmitField('Zapisz')

    def __init__(self, original_nazwa, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_nazwa = original_nazwa

    def validate_username(self, nazwa):
        if nazwa.data != self.original_nazwa:
            user = db.session.scalar(sa.select(User).where(User.nazwa == nazwa.data))
            if user is not None:
                raise ValidationError('Ta nazwa jest zajęta!')
            
class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post = TextAreaField('MÓW.', validators=[
        DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')