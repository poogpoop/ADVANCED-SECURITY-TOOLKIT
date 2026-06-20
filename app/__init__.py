"""
ADVANCED SECURITY TOOLKIT PRO v4.0
Final Working Version
"""

import os
from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    
    # Register ONLY existing blueprints
    from app.systems.vpn_proxy_manager import bp as vpn_bp
    from app.systems.all_systems import init_app as register_core
    
    app.register_blueprint(vpn_bp, url_prefix='/vpn_proxy')
    register_core(app)
    
    return app
