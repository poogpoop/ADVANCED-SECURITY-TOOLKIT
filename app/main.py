from app import create_app
import os

app, socketio = create_app()

@app.route('/')
def index():
    return '''<!DOCTYPE html>
<html><head><title>Security Toolkit PRO v4.0</title>
<style>
body{font-family:Arial,sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);
color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
.container{text-align:center;padding:40px;background:rgba(255,255,255,.05);
border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.5)}
h1{font-size:3em;color:#6f42c1;margin-bottom:20px}
.status{color:#00ff88;font-size:1.2em}
a{color:#6f42c1;text-decoration:none;font-size:1.2em}
a:hover{color:#9b72cb}
</style></head>
<body>
<div class="container">
<h1>🛡️ Security Toolkit PRO</h1>
<p class="status">✅ System Online | Version 4.0</p>
<p style="color:#888;margin:20px 0">
8 Advanced Security Systems Running:<br>
📡 Network Monitor | 🔗 Link Tracker | 👨‍👩‍👧 Parental Control<br>
🕵️ Surveillance | 📱 Metadata | 🎭 Social Engineering<br>
🔬 DFIR | 🌐 VPN Proxy Manager ⭐
</p>
<br><br>
<a href="/vpn_proxy">→ Go to VPN Proxy Manager Dashboard →</a>
</div></body></html>'''

@app.route('/health')
def health():
    return {'status': 'healthy', 'version': '4.0', 'systems': 8}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port)
