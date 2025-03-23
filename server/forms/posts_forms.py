from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, DateTimeLocalField
from wtforms.validators import DataRequired, Length

class NewPostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Contenido')
    publish_date = DateTimeLocalField('Fecha de Publicación (opcional)', format='%Y-%m-%dT%H:%M')
    submit = SubmitField('Crear Post')

class EditPostForm(FlaskForm):
    title = StringField('Título', validators=[DataRequired(), Length(min=2, max=100)])
    content = TextAreaField('Contenido')
    submit = SubmitField('Guardar Cambios')