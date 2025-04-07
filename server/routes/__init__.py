from .admin_routes import admin_bp
from .auth_routes import auth_bp
from .main_routes import main_bp
from .author_routes import author_bp
from .seo_routes import seo_bp
from .health_routes import health_bp

def register_blueprints(app):
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(author_bp)
    app.register_blueprint(health_bp)
    app.register_blueprint(seo_bp)