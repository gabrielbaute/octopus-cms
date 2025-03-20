from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField, DateTimeLocalField
from wtforms.validators import DataRequired, Email, Length

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