from database.db_config import db
from datetime import datetime
from slugify import slugify
from database.models.association_tables import post_tags  # Importamos la tabla de asociación

class Post(db.Model):
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publish_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))
    
    tags = db.relationship('Tag', secondary=post_tags, 
                          backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug:
            self.slug = slugify(self.title)