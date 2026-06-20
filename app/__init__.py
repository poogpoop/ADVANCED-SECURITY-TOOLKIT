import os
from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    
    from app.systems.vpn_proxy_manager import bp as vpn_bp
    from app.systems.new_systems import init_app as register_new
    register_new(app)
    
    return app
