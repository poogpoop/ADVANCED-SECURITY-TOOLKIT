"""
ADVANCED SECURITY TOOLKIT PRO v4.0
All 16 Systems Registered
"""

from flask import Flask
import os

def create_app():
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    
    # Register ALL Blueprints (16 Systems!)
    from app.systems.vpn_proxy_manager import bp as vpn_bp
    from app.systems.analytics import bp as analytics_bp
    from app.systems.users import bp as users_bp
    from app.systems.reports import bp as reports_bp
    
    app.register_blueprint(vpn_bp, url_prefix='/vpn_proxy')
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(reports_bp, url_prefix='/reports')
    
    return app
