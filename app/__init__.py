from flask import Flask
from flask_socketio import SocketIO
import os

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret')
    
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
    
    from app.systems.vpn_proxy_manager import bp as vpn_bp
    app.register_blueprint(vpn_bp, url_prefix='/vpn_proxy')
    
    return app, socketio
