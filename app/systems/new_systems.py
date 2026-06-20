"""
New Systems Bundle: Analytics, Users, Reports
Clean Working Version
"""

from flask import Blueprint, jsonify, request, render_template_string
from datetime import datetime
import random

# ════════════════════════════════════════════════════════
# SYSTEM 9+11+16: ANALYTICS & THEME
# ════════════════════════════════════════════════════════

analytics_bp = Blueprint('analytics', __name__)

analytics_data = {
    "visits": random.randint(500, 2000),
    "users": random.randint(100, 500),
    "systems": {
        "network_monitor": "online",
        "link_tracker": "online",
        "vpn_proxy_manager": "online"
    }
}

@analytics_bp.route('/')
def analytics_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html><head><title>Analytics</title>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body{background:#0f0f23;color:#eee;font-family:sans-serif;padding:20px}
.card{background:#1a1a3e;border-radius:15px;padding:20px;margin-bottom:20px;border:1px solid rgba(111,66,193,.3)}
.stat{background:rgba(111,66,193,.15);border-radius:10px;padding:15px;text-align:center;margin:10px 0}
</style></head><body>
<h3>📊 Dashboard Analytics</h3>
<div class="row"><div class="col-md-4"><div class="stat"><h4 id="visits">--</h4><small>Visits</small></div></div>
<div class="col-md-4"><div class="stat"><h4 id="users">--</h4><small>Users</small></div></div>
<div class="col-md-4"><div class="stat"><h4>99.9%</h4><small>Uptime</small></div></div></div>
<div class="card"><h6>Systems Status</h6><div id="systems"></div></div>
<script>
fetch('/analytics/api/data').then(r=>r.json()).then(d=>{
document.getElementById('visits').textContent=d.visits;
document.getElementById('users').textContent=d.users;
document.getElementById('systems').innerHTML=Object.entries(d.systems).map(([k,v])=>
'<div>'+k.replace(/_/g,' ')+': <span class="badge bg-success">'+v+'</span></div>').join('');
});
</script></body></html>''')

@analytics_bp.route('/api/data')
def analytics_api():
    return jsonify(analytics_data)


# ════════════════════════════════════════════════════════
# SYSTEM 10+12: USERS & NOTIFICATIONS
# ════════════════════════════════════════════════════════

users_bp = Blueprint('users', __name__)

users_list = [{"id":1,"username":"admin","role":"super_admin","status":"active"}]
notifications = [{"id":1,"type":"success","title":"System Online","message":"All systems OK","read":False}]

@users_bp.route('/')
def users_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html><head><title>Users</title>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body{background:#0f0f23;color:#eee;font-family:sans-serif;padding:20px}
.card{background:#1a1a3e;border-radius:15px;padding:20px;margin-bottom:20px;border:1px solid rgba(111,66,193,.3)}
.item{background:rgba(255,255,255,.05);padding:12px;border-radius:8px;margin-bottom:8px}
.notif{border-right:3px solid #6f42c1;padding:12px;border-radius:8px;margin-bottom:8px}
</style></head><body>
<h3>👥 Users & Notifications</h3>
<div class="row"><div class="col-md-6"><div class="card"><h6>Users</h6><div id="ulist"></div></div></div>
<div class="col-md-6"><div class="card"><h6>Notifications (<span id="ncount">0</span>)</h6><div id="nlist"></div></div></div></div>
<script>
fetch('/users/api/data').then(r=>r.json()).then(d=>{
document.getElementById('ncount').textContent=d.notifications.filter(n=>!n.read).length;
document.getElementById('ulist').innerHTML=d.users.map(u=>
'<div class="item">'+u.username+' <span class="badge bg-primary">'+u.role+'</span></div>').join('');
document.getElementById('nlist').innerHTML=d.notifications.map(n=>
'<div class="notif"><strong>'+n.title+'</strong><br><small>'+n.message+'</small></div>').join('');
});
</script></body></html>''')

@users_bp.route('/api/data')
def users_api():
    return {"users": users_list, "notifications": notifications}


# ════════════════════════════════════════════════════════
# SYSTEM 13+14+15: REPORTS & BACKUP & LANGUAGE
# ════════════════════════════════════════════════════════

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/')
def reports_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html><head><title>Reports</title>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body{background:#0f0f23;color:#eee;font-family:sans-serif;padding:20px}
.card{background:#1a1a3e;border-radius:15px;padding:20px;margin-bottom:20px;border:1px solid rgba(111,66,193,.3)}
.item{background:rgba(255,255,255,.05);padding:12px;border-radius:8px;margin-bottom:8px;display:flex;justify-content:space-between}
.lang-btn{padding:8px 18px;border-radius:15px;border:1px solid rgba(255,255,255,.2);background:transparent;color:#fff;cursor:pointer;margin:5px}
.lang-btn.active{background:#6f42c1}
</style></head><body>
<div class="d-flex justify-content-between mb-4">
<h3>📈 Reports & Backups</h3>
<div><button class="lang-btn active" onclick="setLang('ar')">🇸🇦 AR</button><button class="lang-btn" onclick="setLang('en')">🇺🇸 EN</button></div></div>
<div class="row"><div class="col-md-6"><div class="card"><h6>Reports</h6><div id="replist"></div></div></div>
<div class="col-md-6"><div class="card"><h6>Backups</h6><div id="backlist"></div></div></div></div>
<script>
const reports=[{id:1,name:'Security Audit',type:'PDF',size:'2.4 MB'},{id:2,name:'VPN Stats',type:'Excel',size:'1.1 MB'}];
const backups=[{id:1,date:'2024-01-15 02:00',size:'45 MB'},{id:2,date:'2024-01-14 02:00',size:'44 MB'}];
document.getElementById('replist').innerHTML=reports.map(r=>
'<div class="item"><strong>'+r.name+'</strong><span class="badge bg-secondary">'+r.type+' '+r.size+'</span></div>').join('');
document.getElementById('backlist').innerHTML=backups.map(b=>
'<div class="item"><strong>#'+b.id+'</strong><span class="text-muted">'+b.date+' • '+b.size+'</span></div>').join('');
function setLang(l){document.querySelectorAll('.lang-btn').forEach(b=>b.classList.remove('active'));event.target.classList.add('active');}</script></body></html>''')

@reports_bp.route('/api/data')
def reports_api():
    return {"reports": [], "backups": []}


# ════════════════════════════════════════════════════════
# REGISTRATION
# ════════════════════════════════════════════════════════

def init_app(app):
    app.register_blueprint(analytics_bp, url_prefix='/analytics')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(reports_bp, url_prefix='/reports')
