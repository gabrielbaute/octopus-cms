from database.db_config import db
from datetime import datetime
from slugify import slugify

class Post(db.Model):
    __tablename__ = 'post'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    publish_date = db.Column(db.DateTime, nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    slug = db.Column(db.String(100), unique=True, nullable=False)
    author = db.relationship('User', backref=db.backref('posts', lazy=True))

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        if not self.slug:
            self.slug = slugify(self.title)