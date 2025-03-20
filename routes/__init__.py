from .admin_routes import admin_bp
from .auth_routes import auth_bp
from .main_routes import main_bp

def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)