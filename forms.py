from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, SelectField, DateTimeLocalField
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

class NewPostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Contenido')
    publish_date = DateTimeLocalField('Fecha de Publicación (opcional)', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Crear Post')

class ContactForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    subject = StringField('Asunto', validators=[DataRequired(), Length(min=2, max=100)])
    message = TextAreaField('Mensaje', validators=[DataRequired(), Length(min=10)])
    submit = SubmitField('Enviar')

class SubscriptionForm(FlaskForm):
    name = StringField('Nombre', validators=[DataRequired(), Length(min=2, max=50)])
    email = StringField('Correo Electrónico', validators=[DataRequired(), Email()])
    submit = SubmitField('Suscribirse')

class NewsletterForm(FlaskForm):
    subject = StringField('Asunto', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Enviar')
