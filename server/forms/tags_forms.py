from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectMultipleField
from wtforms.validators import DataRequired, Length
from database.models import Tag

class TagForm(FlaskForm):
    name = StringField('Nombre del Tag', validators=[DataRequired(), Length(min=2, max=50)])
    submit = SubmitField('Crear Tag')

class PostTagsForm(FlaskForm):
    tags = SelectMultipleField('Etiquetas', coerce=int)
    
    def __init__(self, *args, **kwargs):
        super(PostTagsForm, self).__init__(*args, **kwargs)
        self.tags.choices = [(tag.id, tag.name) for tag in Tag.query.order_by(Tag.name).all()]