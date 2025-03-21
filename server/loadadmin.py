from flask import current_app
import logging

from database import db
from database.models import User
from config import Config
from werkzeug.security import generate_password_hash

def create_admin_user():
    """Crea el usuario admin, al iniciar el server la primera vez"""
    admin_username = Config.ADMIN_USERNAME
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD

    try:
        if not admin_username or not admin_email or not admin_password:
            current_app.logger.warning(f"Admin credentials not set in environment variables.")
            return

        if User.query.filter_by(email=admin_email).first() is None:
            
            hashed_password = generate_password_hash(admin_password)
            
            admin = User(username=admin_username, email=admin_email, password=hashed_password, role='admin')
            
            db.session.add(admin)
            db.session.commit()
            
            current_app.logger.info(f"Admin user created with username: {admin_username}, email: {admin_email}")

        else:
            current_app.logger.info("Admin user already exists.")
    
    except Exception as e:
        current_app.logger.error(f"No se pudo crear el usuario admin: {e}")