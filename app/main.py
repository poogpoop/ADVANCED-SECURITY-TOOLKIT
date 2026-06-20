"""
ADVANCED SECURITY TOOLKIT PRO v4.0
Main Entry Point - With Core Link
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
.nav{position:fixed;top:20px;right:20px}
.nav a{background:rgba(220,53,69,.2);color:#ff6b6b;padding:10px 20px;border-radius:20px;text-decoration:none;font-size:.9em}
.systems{color:#888;line-height:2.5;margin:25px 0}
a{display:inline-block;margin:12px;padding:14px 35px;background:linear-gradient(135deg,#6f42c1,#6610f2);color:#fff;text-decoration:none;border-radius:50px;transition:all .3s}
a:hover{transform:translateY(-2px);box-shadow:0 10px 25px rgba(111,66,193,.4)}
.btn-all{background:transparent;border:2px solid #6f42c1;color:#6f42c1;padding:15px 40px;border-radius:50px;font-size:1.1em;text-decoration:none;display:inline-block;margin-top:20px;transition:all .3s}
.btn-all:hover{background:#6f42c1;color:#fff;transform:scale(1.05)}
</style></head>
<body>

<div class="nav"><a href="/logout">🚪 Logout</a></div>

<div class="container">
<h1>🛡️ Security Toolkit PRO</h1>
<div style="color:#00ff88;font-size:1.3em;margin:20px 0">✅ Online | v4.0 | 🔒 Protected | <strong>13 Systems Active</strong></div>

<div class="systems"><strong>All 13 Security Systems:</strong><br><br>

📡 Network Monitor &nbsp;|&nbsp; 🔗 Link Tracker<br>
👨‍👩‍👧 Parental Control &nbsp;|&nbsp; 🕵️ Surveillance<br>
📱 Metadata Analyzer &nbsp;|&nbsp; 🎭 Social Engineering<br>
🔬 DFIR Forensics &nbsp;|&nbsp; 🌐 <strong>VPN Proxy Manager ⭐</strong><br><br>

📊 Dashboard Analytics &nbsp;|&nbsp; 👥 User Management<br>
📝 Activity Log &nbsp;|&nbsp; 🔔 Notifications<br>
📈 Reports Generator &nbsp;|&nbsp; 🔄 Backup System<br>
🌐 Multi-Language (AR/EN) &nbsp;|&nbsp; 🎨 Theme Switcher
</div><br>

<a href="/vpn_proxy">🌐 VPN Proxy Manager</a>
<a href="/analytics">📊 Dashboard Analytics</a>
<a href="/users">👥 Users & Notifications</a>
<a href="/reports">📈 Reports & Backups</a>

<br>
<a href="/core" class="btn-all">📋 View All 13 Systems Dashboard →</a>

</div></body></html>'''


@app.route('/health')
def health():
    return {'status': 'healthy', 'version': '4.0', 'systems': 13}, 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
