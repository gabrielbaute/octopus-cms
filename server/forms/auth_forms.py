from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, SelectField
from wtforms.validators import DataRequired, Email, EqualTo, Length

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('author', 'Author'), ('admin', 'Admin')], validators=[DataRequired()])
    submit = SubmitField('Create')

class ForgotPasswordForm(FlaskForm):
    email = StringField('Correo electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Enviar link')

class ResetPasswordForm(FlaskForm):
    password = PasswordField('Nueva contraseña', validators=[DataRequired()])
    confirm_password = PasswordField('Confirmar nueva contraseña', validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Reestablecer contraseña')
