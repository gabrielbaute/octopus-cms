from flask import Flask, render_template
from flask_migrate import Migrate

from config import Config, create_initial_super_admin, initialize_permissions_system
from database import init_db, db
from database.models import User
from mail import mail
from server_logging import setup_logging

from server.routes import register_blueprints
from server.server_extensions import login_manager
from server.errors_handler import register_error_handlers


def create_app():
    """Función constructora de la aplicación"""
    app = Flask(__name__,
                template_folder='../templates',
                static_folder='../static')
    
    app.config.from_object(Config)

    # Inicializando componentes
    init_db(app)
    mail.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    migrate = Migrate(app, db)
    setup_logging(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    register_blueprints(app)
    print("BluePrints registrados") # Para debugging
    register_error_handlers(app)
    print("Error handlers registrados")

    with app.app_context():
        db.create_all()
        initialize_permissions_system()
        create_initial_super_admin()
        app.logger.info(f"Server listening on port: {Config.PORT}")

    # Hacer que APP_NAME esté disponible globalmente en las plantillas
    @app.context_processor
    def inject_app_name():
        return {
            "app_name": app.config["APP_NAME"],
            "cms_version": app.config["CMS_VERSION"],
            "server_language": app.config["LANGUAGE"]
            }

    return app