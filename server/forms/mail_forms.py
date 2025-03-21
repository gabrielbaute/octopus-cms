from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class NewsletterForm(FlaskForm):
    subject = StringField('Asunto', validators=[DataRequired(), Length(min=2, max=100)])
    submit = SubmitField('Enviar')