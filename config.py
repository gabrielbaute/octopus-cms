"""Configuración de la aplicación Flask."""

import os
from dotenv import load_dotenv
from datetime import timedelta

load_dotenv()

BASE_DIR=os.path.abspath(os.path.dirname(__file__))

# Función para convertir una cadena a un valor booleano
def str_to_bool(value):
    return value.lower() in ['true', '1', 'yes']

class Config:
    """Configuración de la aplicación Flask."""
    
    # Flask server
    BASEDIR=BASE_DIR
    BLOG_NAME=os.getenv('APP_NAME', 'MyApp')
    PORT=os.environ.get("PORT")
    DEBUG=os.environ.get("DEBUG")
    SCHEDULER_API_ENABLED=os.environ.get("SCHEDULER_API_ENABLED") or True

    # Variables de entorno para el administrador
    ADMIN_USERNAME=os.environ.get('ADMIN_USERNAME') or 'admin'
    ADMIN_EMAIL=os.environ.get('ADMIN_EMAIL') or 'admin@example.com'
    ADMIN_PASSWORD=os.environ.get('ADMIN_PASSWORD') or 'admin_password'

    # SQLAlchemy
    SQLALCHEMY_DATABASE_URI=os.environ.get('SQLALCHEMY_DATABASE_URI') or f'sqlite:///{os.path.join(BASE_DIR, "yourdatabase.db")}'
    SQLALCHEMY_TRACK_MODIFICATIONS=os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS') or False

    # Configuración de Flask-Mail
    MAIL_SERVER = os.environ.get('MAIL_SERVER')
    MAIL_PORT = os.environ.get('MAIL_PORT')
    MAIL_USE_TLS = str_to_bool(os.environ.get('MAIL_USE_TLS', 'False'))
    MAIL_USE_SSL = str_to_bool(os.environ.get('MAIL_USE_SSL', 'False'))
    MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')
    MAIL_DEBUG = int(os.environ.get('MAIL_DEBUG', 0))