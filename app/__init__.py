import os
from flask import Flask

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    
    from app.systems.vpn_proxy_manager import bp as vpn_bp
    from app.systems.all_systems import init_app as register_core
    from app.systems.network_monitor import init_app as register_network  # ←← هذا لازم يكون موجود!
    
    app.register_blueprint(vpn_bp, url_prefix='/vpn_proxy')
    register_core(app)
    register_network(app)  # ←←← هذا لازم يكون موجود!
    
    return app
