from flask import current_app
from database import db
from database.models import User
from config.config import Config
from werkzeug.security import generate_password_hash

def create_initial_super_admin():
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
            
            super_admin = User(
                username=admin_username,
                email=admin_email,
                password=hashed_password,
                role='super_admin',
                is_active=True)
            
            db.session.add(super_admin)
            db.session.commit()
            
            current_app.logger.info(f"Super admin user created with username: {admin_username}, email: {admin_email}")

        else:
            current_app.logger.info("Admin user already exists.")
    
    except Exception as e:
        current_app.logger.error(f"No se pudo crear el usuario admin: {e}")