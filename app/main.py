"""
ADVANCED SECURITY TOOLKIT PRO v4.0
Main Entry Point - With Password Protection
"""

from functools import wraps
from flask import request, redirect, Response, session, url_for
from app import create_app
import os

# Create app
app = create_app()

# ═══════════════════════════════════════════════════════════════
# 🔐 PASSWORD PROTECTION CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# ⚠️ CHANGE THESE CREDENTIALS!
USERNAME = os.environ.get('ADMIN_USERNAME', 'admin')
PASSWORD = os.environ.get('ADMIN_PASSWORD', 'Security2024!')


def check_auth(username, password):
    """Check if username/password is correct"""
    return username == USERNAME and password == PASSWORD


def authenticate():
    """Send 401 response"""
    return Response(
        '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>🔒 Security Toolkit - Login Required</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body {
            font-family: 'Segoe UI', Tahoma, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #fff;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-box {
            background: rgba(255,255,255,0.05);
            padding: 40px;
            border-radius: 20px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
            text-align: center;
            max-width: 400px;
            width: 90%;
            border: 1px solid rgba(111,66,193,0.3);
        }
        h2 { color: #6f42c1; margin-bottom: 10px; }
        p { color: #888; margin-bottom: 25px; }
        input {
            width: 100%;
            padding: 15px;
            margin: 10px 0;
            border: 1px solid rgba(111,66,193,0.3);
            border-radius: 10px;
            background: rgba(255,255,255,0.05);
            color: #fff;
            font-size: 16px;
        }
        button {
            width: 100%;
            padding: 15px;
            background: linear-gradient(135deg, #6f42c1, #6610f2);
            color: white;
            border: none;
            border-radius: 10px;
            font-size: 18px;
            cursor: pointer;
            margin-top: 15px;
            transition: transform 0.3s;
        }
        button:hover { transform: scale(1.02); }
        .lock-icon { font-size: 60px; margin-bottom: 20px; }
        .error { color: #ff6b6b; margin-top: 15px; display: none; }
    </style>
</head>
<body>
    <div class="login-box">
        <div class="lock-icon">🔐</div>
        <h2>Security Toolkit PRO</h2>
        <p>Enter your credentials to access</p>
        
        <form action="" method="POST">
            <input type="text" name="username" placeholder="Username" required autofocus>
            <input type="password" name="password" placeholder="Password" required>
            <button type="submit">🔓 Login</button>
        </form>
        
        <p class="error" id="error">❌ Invalid credentials!</p>
    </div>
    
    <script>
        // Show error if URL has ?error=1
        if (window.location.search.includes('error=1')) {
            document.getElementById('error').style.display = 'block';
        }
    </script>
</body>
</html>
        ''',
        401,
        {'WWW-Authenticate': 'Basic realm="Security Toolkit PRO"'}


def requires_auth(f):
    """Decorator for password protection"""
    @wraps(f)
    def decorated(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return decorated


# ═══════════════════════════════════════════════════════════════
# ROUTES
# ═══════════════════════════════════════════════════════════════


@app.route('/login', methods=['GET', 'POST'])
def login():
    """Custom login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if check_auth(username, password):
            session['logged_in'] = True
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login') + '?error=1')
    
    return authenticate()


@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    return redirect(url_for('login'))


@app.route('/')
@requires_auth
def index():
    '''Main Landing Page'''
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Security Toolkit PRO v4.0</title>
    <meta charset="UTF-8">
    <style>
        body {
            font-family: 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #fff;
            min-height: 100vh;
            margin: 0;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .container {
            text-align: center;
            padding: 50px;
            background: rgba(255,255,255,0.05);
            border-radius: 25px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.5);
        }
        h1 { color: #6f42c1; font-size: 3em; }
        .status { color: #00ff88; margin: 20px 0; }
        a {
            display: inline-block;
            margin-top: 30px;
            padding: 15px 40px;
            background: linear-gradient(135deg, #6f42c1, #6610f2);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            transition: all 0.3s;
        }
        a:hover { transform: translateY(-3px); box-shadow: 0 10px 30px rgba(111,66,193,0.5); }
        .nav { position: fixed; top: 20px; right: 20px; }
        .nav a { 
            background: rgba(220,53,69,0.2); 
            color: #ff6b6b; 
            padding: 10px 20px; 
            border-radius: 20px;
            font-size: 14px;
            margin-top: 0;
        }
        .systems { color: #888; line-height: 2.2; margin: 25px 0; }
    </style>
</head>
<body>
    <div class="nav">
        <a href="/logout">🚪 Logout</a>
    </div>
    
    <div class="container">
        <h1>🛡️ Security Toolkit PRO</h1>
        <div class="status">✅ System Online | Version 4.0 | Protected 🔒</div>
        
        <div class="systems">
            <strong>8 Advanced Security Systems:</strong><br><br>
            📡 Network Monitor &nbsp;|&nbsp; 🔗 Link Tracker<br>
            👨‍👩‍👧 Parental Control &nbsp;|&nbsp; 🕵️ Surveillance<br>
            📱 Metadata Analyzer &nbsp;|&nbsp; 🎭 Social Engineering<br>
            🔬 DFIR Forensics &nbsp;|&nbsp; 🌐 <strong>VPN Proxy Manager ⭐</strong>
        </div>
        
        <a href="/vpn_proxy">→ Go to VPN Proxy Manager →</a>
    </div>
</body>
</html>
'''


@app.route('/health')
def health_check():
    '''Health check (public, no auth required)'''
    return {'status': 'healthy', 'version': '4.0', 'protected': True}, 200


@app.route('/vpn_proxy')
@requires_auth
def vpn_redirect():
    '''Redirect to VPN manager with auth'''
    from flask import redirect, url_for
    return redirect('/vpn_proxy/')


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
