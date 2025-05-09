from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()], render_kw={"size": 32})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={"size": 32})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')