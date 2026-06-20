"""
Core Systems Bundle: Systems 1-7
Network Monitor, Link Tracker, Parental Control,
Surveillance, Metadata Analyzer, Social Engineering, DFIR
"""

from flask import Blueprint, jsonify, request, render_template_string
from datetime import datetime
import random
import re

# ════════════════════════════════════════════════════════
# SYSTEM 1: NETWORK MONITOR
# ════════════════════════════════════════════════════════

network_bp = Blueprint('network', __name__)

network_stats = {
    "packets_captured": random.randint(1000, 5000),
    "active_connections": random.randint(10, 50),
    "bandwidth_usage": f"{random.uniform(50, 500):.1} MB/s",
    "threats_blocked": random.randint(0, 5),
    "protocols": {"TCP": 45, "UDP": 30, "HTTP": 15, "HTTPS": 10},
    "top_ips": ["192.168.1." + str(random.randint(1, 254)) for _ in range(5)],
    "alerts": [
        {"time": "2 min ago", "type": "warning", "msg": "Unusual traffic from 203.0.113.45"},
        {"time": "15 min ago", "type": "info", "msg": "New device detected"},
        {"time": "1 hour ago", "type": "danger", "msg": "Port scan detected"}
    ]
}

@network_bp.route('/')
def network_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html><head><title>📡 Network Monitor</title>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
<style>body{background:#0f0f23;color:#eee;font-family:sans-serif;padding:20px}
.card{background:#1a1a3e;border-radius:15px;padding:20px;margin-bottom:20px;border:1px solid rgba(111,66,193,.3)}
.stat{background:rgba(111,66,193,.15);border-radius:12px;padding:18px;text-align:center}
.alert-item{background:rgba(255,255,255,.03);border-right:3px solid #ffc107;padding:12px;border-radius:6px;margin-bottom:8px;font-size:.9em}
.alert-danger{border-color:#dc3545}.alert-warning{border-color:#ffc107}.alert-info{border-color:#17a2b8}
</style></head><body>
<h3><i class="bi bi-router me-2"></i>Network Monitor</h3>
<div class="row g-3 mb-4">
<div class="col-md-3"><div class="stat"><h4 id="packets">--</h4><small>Packets Captured</small></div></div>
<div class="col-md-3"><div class="stat"><h4 id="connections">--</h4><small>Active Connections</small></div></div>
<div class="col-md-3"><div class="stat"><h4 id="bandwidth">--</h4><small>Bandwidth</small></div></div>
<div class="col-md-3"><div class="stat"><h4 id="threats">--</h4><small>Threats Blocked</small></div></div>
</div>
<div class="row g-4">
<div class="col-md-6"><div class="card"><h6>Traffic by Protocol</h6><div id="protocols"></div></div></div>
<div class="col-md-6"><div class="card"><h6>Recent Alerts <span class="badge bg-danger ms-2" id="alertcount">0</span></h6><div id="alerts"></div></div></div>
</div>
<script>
fetch('/network/api/stats').then(r=>r.json()).then(d=>{
document.getElementById('packets').textContent=d.packets_captured;
document.getElementById('connections').textContent=d.active_connections;
document.getElementById('bandwidth').textContent=d.bandwidth_usage;
document.getElementById('threats').textContent=d.threats_blocked;
document.getElementById('alertcount').textContent=d.alerts.length;
document.getElementById('protocols').innerHTML=Object.entries(d.protocols).map(([k,v])=>
'<div class="d-flex justify-content-between mb-2"><span>'+k+'</span><div class="progress" style="height:8px;width:100px"><div class="progress-bar bg-primary" style="width:'+v+'%"></div></div></div>').join('');
document.getElementById('alerts').innerHTML=d.alerts.map(a=>
'<div class="alert-item alert-'+a.type+'"><small class="text-muted">'+a.time+'</small> '+a.msg+'</div>').join('');
});
</script></body></html>''')

@network_bp.route('/api/stats')
def network_api():
    return jsonify(network_stats)


# ════════════════════════════════════════════════════════
# SYSTEM 2: LINK TRACKER
# ════════════════════════════════════════════════════════

tracker_bp = Blueprint('tracker', __name__)

links_db = [
    {"id": 1, "short_code": "abc123", "original_url": "https://example.com/page1", "clicks": 45, "created": "2024-01-15", "status": "active"},
    {"id": 2, "short_code": "xyz789", "original_url": "https://google.com/search", "clicks": 128, "created": "2024-01-14", "status": "active"},
    {"id": 3, "short_code": "link456", "original_url": "https://github.com/repo", "clicks": 23, "created": "2024-01-13", "status": "expired"},
]

@tracker_bp.route('/')
def tracker_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html><head><title>🔗 Link Tracker</title>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body{background:#0f0f23;color:#eee;font-family:sans-serif;padding:20px}
.card{background:#1a1a3e;border-radius:15px;padding:20px;margin-bottom:20px;border:1px solid rgba(111,66,193,.3)}
.link-row{background:rgba(255,255,255,.03);padding:15px;border-radius:10px;margin-bottom:10px;display:flex;justify-content:space-between;align-items:center}
</style></head><body>
<h3><i class="bi bi-link-45deg me-2"></i>Link Tracker</h3>
<div class="card"><h6>Create Short Link</h6>
<div class="input-group mb-3"><input type="text" class="form-control" id="urlInput" placeholder="Paste URL to shorten...">
<button class="btn btn-primary" onclick="createLink()">Shorten</button></div></div>

<h6>Your Links (<span id="count">0</span>)</h6><div id="links"></div></div>
<script>
function loadLinks(){fetch('/tracker/api/links').then(r=>r.json()).then(d=>{
document.getElementById('count').textContent=d.length;
document.getElementById('links').innerHTML=d.map(l=>
'<div class="link-row"><div><strong>/go/'+l.short_code+'</strong><br><small class="text-muted">'+l.original_url[:50]+'...</small></div>'+
'<div><span class="badge bg-primary">'+l.clicks+' clicks</span> <span class="badge bg-'+(l.status==='active'?'success':'secondary')+'">'+l.status+'</span></div></div>').join('');
});}
async function createLink(){const url=document.getElementById('urlInput').value;if(!url)return alert('Enter URL');
await fetch('/tracker/api/create',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({url})});
document.getElementById('urlInput').value='';loadLinks();}
loadLinks();
</script></body></html>''')

@tracker_bp.route('/api/links')
def tracker_links():
    return jsonify(links_db)

@tracker_bp.route('/api/create', methods=['POST'])
def tracker_create():
    data = request.json or {}
    new_link = {
        "id": len(links_db) + 1,
        "short_code": ''.join(random.choices('abcdefghijklmnopqrstuvwxyz0123456789', k=6)),
        "original_url": data.get("url", ""),
        "clicks": 0,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "status": "active"
    }
    links_db.insert(0, new_link)
    return jsonify({"success": True, "link": new_link})


# ════════════════════════════════════════════════════════
# SYSTEM 3: PARENTAL CONTROL
# ════════════════════════════════════════════════════════

parental_bp = Blueprint('parental', __name__)

parental_rules = {
    "web_filtering": {"enabled": True, "blocked_sites": ["facebook.com", "twitter.com", "instagram.com"], "mode": "strict"},
    "time_limits": {"enabled": True, "max_hours_per_day": 4, "bedtime_start": "22:00", "bedtime_end": "06:00"},
    "content_filter": {"enabled": True, "block_adult": True, "block_violence": True, "block_gambling": True},
    "activity_monitor": {"enabled": True, "log_searches": True, "log_social": True}
}

@parental_bp.route('/')
def parental_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html><head><title>👨‍👩‍👧 Parental Control</title>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
<style>body{background:#0f0f23;color:#eee;font-family:sans-serif;padding:20px}
.card{background:#1a1a3e;border-radius:15px;padding:20px;margin-bottom:20px;border:1px solid rgba(111,66,193,.3)}
.rule{display:flex;justify-content:space-between;align-items:center;background:rgba(255,255,255,.03);padding:15px;border-radius:10px;margin-bottom:10px}
.toggle{position:relative;width:50px;height:26px;background:#555;border-radius:13px;cursor:pointer}
.toggle.active{background:#198754}.toggle::after{content:'';position:absolute;top:3px;left:3px;width:20px;height:20px;background:#fff;border-radius:50%;transition:.3s}
.toggle.active::after{transform:translateX(24px)}
</style></head><body>
<h3><i class="bi bi-shield-lock me-2"></i>Parental Control</h3>
<div class="row g-4">
<div class="col-md-6"><div class="card"><h6>🌐 Web Filtering</h6><div class="rule"><span>Block Social Media</span><div class="toggle active" onclick="this.classList.toggle('active')"></div></div>
<div class="rule"><span>Block Adult Content</span><div class="toggle active" onclick="this.classList.toggle('active')"></div></div>
<div class="rule"><span>Block Gambling</span><div class="toggle active" onclick="this.classList.toggle('active')"></div></div></div></div>
<div class="col-md-6"><div class="card"><h6>⏰ Time Limits</h6><div class="rule"><span>Daily Limit: 4 hours</span><div class="toggle active" onclick="this.classList.toggle('active')"></div></div>
<div class="rule"><span>Bedtime Mode (22:00-06:00)</span><div class="toggle active" onclick="this.classList.toggle('active')"></div></div></div></div>
<div class="col-md-12"><div class="card"><h6>📋 Blocked Sites List</h6><div id="blocked-list"></div></div></div>
</div>
<script>
const blocked=["facebook.com","twitter.com","instagram.com","tiktok.com","reddit.com","pornhub.com","gambling.com"];
document.getElementById('blocked-list').innerHTML=blocked.map(b=>
'<span class="badge bg-danger me-2 mb-2">'+
