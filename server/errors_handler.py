from flask import render_template, current_app

def register_error_handlers(app):
    """Registra handlers de errores personalizados."""
    
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(403)
    def forbidden_route(e):
        return render_template('errors/403.html'), 404