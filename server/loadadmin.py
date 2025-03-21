from database import db
from database.models import User
from config import Config
from .server_extensions import bcrypt

def create_admin_user():
    """Crea el usuario admin, al iniciar el server la primera vez"""
    admin_username = Config.ADMIN_USERNAME
    admin_email = Config.ADMIN_EMAIL
    admin_password = Config.ADMIN_PASSWORD

    try:
        if not admin_username or not admin_email or not admin_password:
            print("Admin credentials not set in environment variables.")
            return

        if User.query.filter_by(email=admin_email).first() is None:
            hashed_password = bcrypt.generate_password_hash(admin_password).decode('utf-8')
            admin = User(username=admin_username, email=admin_email, password=hashed_password, role='admin')
            db.session.add(admin)
            db.session.commit()
            print("Admin user created.")
        else:
            print("Admin user already exists.")
    
    except Exception as e:
        print(f"No se pudo crear el usuario admin: {e}")