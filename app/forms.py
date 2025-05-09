from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    nazwa = StringField('Nazwa', validators=[DataRequired()])
    haslo = PasswordField('Hasło', validators=[DataRequired()])
    pamietaj_mnie = BooleanField('Pamiętaj Mnie')
    submit = SubmitField('Zarejestruj Się')