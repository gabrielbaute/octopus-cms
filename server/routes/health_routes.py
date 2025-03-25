# server/routes/health.py
from flask import Blueprint, jsonify
from sqlalchemy import text
from database import db
from config import Config

health_bp = Blueprint('health', __name__)

@health_bp.route('/health')
def health_check():
    try:
        # Verificar conexión a la base de datos (opcional pero recomendado)
        db.session.execute(text('SELECT 1'))
        return jsonify({
            "status": "healthy",
            "version": Config.CMS_VERSION,
            "database": "connected"
        }), 200
    except Exception as e:
        return jsonify({
            "status": "unhealthy",
            "error": str(e)
        }), 500