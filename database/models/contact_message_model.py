from database.db_config import db
from datetime import datetime

class ContactMessage(db.Model):
    __tablename__ = 'contactmessage'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_sent = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)