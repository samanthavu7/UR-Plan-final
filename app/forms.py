from flask_wtf import Form
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length, AnyOf

class LoginForm(Form):
	username = StringField('Email', validators=[InputRequired(), Email(message='Invalid Email!')])
	password = PasswordField('Password', validators=[InputRequired(), Length(min=5, max=10), AnyOf(['secret', 'password'])])