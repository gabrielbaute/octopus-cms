# seo/seo_routes.py
from flask import Blueprint, render_template, Response
from datetime import datetime
from database.models import Post

seo_bp = Blueprint('seo', __name__)

@seo_bp.route('/sitemap.xml')
def sitemap():
    # Obtener posts públicos ordenados por fecha (del más nuevo al más viejo)
    posts = Post.query.filter(
        Post.publish_date <= datetime.utcnow()
    ).order_by(Post.publish_date.desc()).all()
    
    # URLs estáticas importantes
    static_urls = [
        {'loc': 'main.index', 'priority': '1.0', 'changefreq': 'daily'},
        {'loc': 'main.blog', 'priority': '0.9', 'changefreq': 'daily'},
        {'loc': 'main.about', 'priority': '0.7', 'changefreq': 'monthly'},
    ]
    
    return render_template('seo/sitemap.xml', 
                         posts=posts,
                         static_urls=static_urls,
                         now=datetime.utcnow().strftime('%Y-%m-%d'))

@seo_bp.route('/robots.txt')
def robots():
    return render_template('seo/robots.txt'), 200, {'Content-Type': 'text/plain'}