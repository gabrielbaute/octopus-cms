import requests
from flask import current_app, url_for
from datetime import datetime

def ping_google():
    try:
        sitemap_url = url_for('seo.sitemap', _external=True, _scheme='https')
        ping_url = f"https://www.google.com/ping?sitemap={sitemap_url}"
        
        response = requests.get(ping_url)
        response.raise_for_status()
        
        current_app.logger.info(f"Google pinged successfully at {datetime.utcnow()}")
        return True
    except Exception as e:
        current_app.logger.error(f"Google ping failed: {str(e)}")
        return False