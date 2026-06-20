"""
ADVANCED SECURITY TOOLKIT PRO v4.0
Main Application Package
"""

from flask import Flask
import os

def create_app():
    """Application Factory - Simple Version for Render"""
    
    app = Flask(__name__,
                template_folder='templates',
                static_folder='static')
    
    # Config
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-change-me')
    
    # Register Blueprints (Systems)
    from app.systems.vpn_proxy_manager import bp as vpn_bp
    app.register_blueprint(vpn_bp, url_prefix='/vpn_proxy')
    
    return app
