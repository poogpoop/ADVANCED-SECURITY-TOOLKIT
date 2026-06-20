"""
ADVANCED SECURITY TOOLKIT PRO v4.0
Simple Version
"""

import os
from app import create_app

app = create_app()


@app.route('/')
def index():
    return '''
<!DOCTYPE html>
<html><head><title>Security Toolkit PRO v4.0</title>
<meta charset="UTF-8">
<style>
body{font-family:'Segoe UI',sans-serif;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;min-height:100vh;margin:0;display:flex;align-items:center;justify-content:center}
.container{text-align:center;padding:50px;background:rgba(255,255,255,.05);border-radius:25px;box-shadow:0 20px 60px rgba(0,0,0,.5)}
h1{color:#6f42c1;font-size:3em;margin-bottom:15px}
a{display:inline-block;margin:20px;padding:15px 40px;background:linear-gradient(135deg,#6f42c1,#6610f2);color:#fff;text-decoration:none;border-radius:50px}
a:hover{transform:translateY(-3px)}
.systems{color:#888;line-height:2.2;margin:25px 0}
</style></head><body>
<div class="container">
<h1>🛡️ Security Toolkit PRO</h1>
<div style="color:#00ff88;font-size:1.3em;margin:20px 0">✅ System Online | Version 4.0 | 16 Systems Active</div>

<div class="systems"><strong>All Systems:</strong><br><br>

📡 Network Monitor &nbsp;|&nbsp; 🔗 Link Tracker<br>
👨‍👩‍👧 Parental Control &nbsp;|&nbsp; 🕵️ Surveillance<br>
📱 Metadata Analyzer &nbsp;|&nbsp; 🎭 Social Engineering<br>
🔬 DFIR Forensics &nbsp;|&nbsp; 🌐 <strong>VPN Proxy Manager ⭐</strong><br><br>

📊 Dashboard Analytics &nbsp;|&nbsp; 👥 User Management<br>
📝 Activity Log &nbsp;|&nbsp; 🔔 Notifications<br>
📈 Reports Generator &nbsp;|&nbsp; 🔄 Backup System<br>
🌐 Multi-Language (AR/EN) &nbsp;|&nbsp; 🎨 Theme Switcher
</div><br>

<a href="/vpn_proxy">🌐 VPN Manager</a><br><br>
<a href="/analytics">📊 Analytics Dashboard</a><br><br>
<a href="/users">👥 Users & Notifications</a><br><br>
<a href="/reports">📈 Reports & Backups</a>
</div></body></html>'''


@app.route('/health')
def health():
    return {'status': 'healthy', 'version': '4.0', 'systems': 16}, 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
