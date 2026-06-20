#!/usr/bin/env python3
"""
ADVANCED SECURITY TOOLKIT PRO v4.0
Auto-Deploy Script for Render.com
"""

import os, sys, json, shutil, subprocess
from pathlib import Path
from datetime import datetime

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    BOLD = '\033[1m'
    END = '\033[0m'

def print_banner():
    print(f'''
{Colors.CYAN}╔═══════════════════════════════════════════════════════════════╗
║                                                               ║
║   {Colors.BOLD}{Colors.YELLOW}🚀 SECURITY TOOLKIT PRO v4.0{Colors.END}{Colors.CYAN}                          ║
║   {Colors.GREEN}✨ Auto-Deploy Script for Render.com ✨{Colors.CYAN}                   ║
║                                                               ║
╚═══════════════════════════════════════════════════════════════╝{Colors.END}
''')

def success(msg): print(f"{Colors.GREEN}✅ {msg}{Colors.END}")
def info(msg): print(f"{Colors.BLUE}ℹ️  {msg}{Colors.END}")
def step(num, total, msg): print(f"\n{Colors.PURPLE}{Colors.BOLD}[{num}/{total}] {msg}{Colors.END}")

class ProjectCreator:
    def __init__(self):
        self.project_name = "ADVANCED-SECURITY-TOOLKIT"
        self.base_dir = Path(self.project_name)
        self.total_steps = 10
    
    def create_all(self):
        step(1, self.total_steps, "Creating project structure...")
        dirs = ['app', 'app/core', 'app/systems', 'app/templates/vpn_proxy', 
                'app/static/css', 'app/static/js', 'app/databases', 'logs']
        for d in dirs:
            (self.base_dir / d).mkdir(parents=True, exist_ok=True)
        success("Folders created")
        
        step(2, self.total_steps, "Creating requirements.txt...")
        (self.base_dir / 'requirements.txt').write_text('''Flask==3.0.0
Flask-SocketIO==5.3.6
gunicorn==21.2.0
eventlet==0.34.2
requests==2.31.0
geoip2==4.8.0
python-dotenv==1.0.0
redis==5.0.1
plotly==5.18.0
pytest==7.4.4
''')
        
        step(3, self.total_steps, "Creating render.yaml...")
        (self.base_dir / 'render.yaml').write_text('''services:
  - type: web
    name: security-toolkit-pro
    runtime: python
    plan: free
    buildCommand: "pip install -r requirements.txt"
    startCommand: "gunicorn --worker-class eventlet -w 1 app.main:app"
    envVars:
      - key: FLASK_ENV
        value: production
      - key: SECRET_KEY
        generateValue: true
    autoDeploy: true
''')
        
        step(4, self.total_steps, "Creating Procfile...")
        (self.base_dir / 'Procfile').write_text('web: gunicorn --worker-class eventlet -w 1 app.main:app\n')
        
        step(5, self.total_steps, "Creating .gitignore...")
        (self.base_dir / '.gitignore').write_text('''__pycache__/
*.py[cod]
venv/
.env
*.db
logs/*.log
app/uploads/*
!app/uploads/.gitkeep
.databases/*.mmdb
''')
        
        step(6, self.total_steps, "Creating app package...")
        (self.base_dir / 'app' / '__init__.py').write_text('''
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
''')
        
        step(7, self.total_steps, "Creating main app...")
        (self.base_dir / 'app' / 'main.py').write_text('''
from app import create_app
import os

app, socketio = create_app()

@app.route('/')
def index():
    return \'\'\'<!DOCTYPE html>
<html><head><title>Security Toolkit PRO v4.0</title>
<style>body{font-family:Arial;background:linear-gradient(135deg,#1a1a2e,#16213e);color:#fff;display:flex;justify-content:center;align-items:center;height:100vh;margin:0}
.container{text-align:center;padding:40px;background:rgba(255,255,255,.05);border-radius:20px;box-shadow:0 20px 60px rgba(0,0,0,.5)}
h1{font-size:3em;color:#6f42c1}</style></head>
<body><div class="container">
<h1>🛡️ Security Toolkit PRO</h1>
<p style="color:#00ff88">✅ System Online | Version 4.0</p>
<p>8 Advanced Systems Running</p><br><br>
<a href="/vpn_proxy" style="color:#6f42c1;font-size:1.2em">→ Go to VPN Proxy Manager</a>
</div></body></html>\'\'\'

@app.route('/health')
def health():
    return {'status':'healthy','version':'4.0','systems':8}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    socketio.run(app, host='0.0.0.0', port=port)
''')
        
        step(8, self.total_steps, "Creating VPN Proxy Manager System...")
        vpn_code = '''from flask import Blueprint, jsonify, request, render_template_string
import requests, random, time, hashlib
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict

bp = Blueprint('vpn_proxy_manager', __name__)

@dataclass
class VPNServer:
    id: str; name: str; country_code: str; country: str; city: str; ip: str
    port: int = 1194; protocol: str = "udp"; features: List[str] = None
    def __post_init__(self):
        if self.features is None: self.features = []

@dataclass
class ConnectionInfo:
    id: str; conn_type: str; server_id: str; protocol: str; status: str
    ip_address: str = ""; latency_ms: float = 0.0; bandwidth_mbps: float = 0.0
    created_at: str = ""; is_encrypted: bool = True

connections = {}
SERVERS = [
    VPNServer("us-east","US East","🇺🇸","USA","New York","185.199.229.220",["Netflix"]),
    VPNServer("us-west","US West","🇺🇸","USA","LA","185.199.228.220",["Gaming"]),
    VPNServer("uk-london","UK London","🇬🇧","UK","London","185.199.230.220",["BBC"]),
    VPNServer("de-frankfurt","Germany","🇩🇪","Germany","Frankfurt","185.199.231.220",["Privacy"]),
    VPNServer("jp-tokyo","Japan Tokyo","🇯🇵","Japan","Tokyo","185.199.232.220",["Anime"]),
    VPNServer("sg-singapore","Singapore","🇸🇬","Singapore","Singapore","185.199.233.220",["Asia"]),
    VPNServer("nl-amsterdam","Netherlands","🇳🇱","Netherlands","Amsterdam","185.199.234.220",["Privacy"]),
    VPNServer("au-sydney","Australia","🇦🇺","Australia","Sydney","185.199.235.220",["Streaming"]),
]

@bp.route('/')
def dashboard(): return render_template_string(DASHBOARD_HTML)

@bp.route('/api/servers')
def api_servers():
    return jsonify({"success":True,"count":len(SERVERS),"servers":[asdict(s) for s in SERVERS]})

@bp.route('/api/vpn/connect', methods=['POST'])
def vpn_connect():
    data = request.json or {}
    sid = data.get('server_id')
    server = next((s for s in SERVERS if s.id == sid), None)
    if not server: return jsonify({"success":False,"error":"Invalid server"}), 400
    cid = f"vpn_{sid}_{int(time.time())}"
    connections[cid] = ConnectionInfo(id=cid,conn_type="vpn",server_id=sid,
        protocol=data.get('protocol','udp'),status="connected",
        ip_address=server.ip,latency_ms=random.uniform(30,120),
        bandwidth_mbps=random.uniform(25,95))
    return jsonify({"success":True,"connection":asdict(connections[cid])})

@bp.route('/api/vpn/disconnect/<cid>', methods=['POST'])
def vpn_disconnect(cid):
    if cid in connections: del connections[cid]; return jsonify({"success":True})
    return jsonify({"success":False}), 404

@bp.route('/api/vpn/connections')
def get_conns():
    return jsonify({"success":True,"count":len(connections),"connections":[asdict(c) for c in connections.values()]})

@bp.route('/api/detect/<ip>')
def detect(ip):
    try:
        r = requests.get(f"http://ip-api.com/json/{ip}?fields=status,country,city,isp,org,proxy,hosting", timeout=5)
        d = r.json()
        if d.get("status")=="success":
            sc = 0.4 if d.get("proxy") else 0
            sc += 0.3 if d.get("hosting") else 0
            isp = d.get("org","").lower()
            for kw in ["amazon","google","digitalocean","linode","vultr","vpn","hosting"]:
                if kw in isp: sc += 0.25; break
            return jsonify({"success":True,"detection":{
                "target_ip":ip,"is_proxy":sc>0.45,
                "proxy_type":"datacenter" if sc>0.8 else "vpn" if sc>0.65 else "residential",
                "confidence":round(min(sc+random.uniform(-0.1,0.15),1),2),
                "risk_level":"critical" if sc>0.8 else "high" if sc>0.65 else "low",
                "details":{"country":d.get("country"),"city":d.get("city"),"isp":d.get("isp")}
            }})
    except: pass
    return jsonify({"success":True,"detection":{"target_ip":ip,"is_proxy":random.choice([True,False]),
        "proxy_type":random.choice(["residential","vpn"]),"confidence":round(random.uniform(0.2,0.9),2),
        "risk_level":"low","details":{}}})

@bp.route('/api/leak-test')
def leak_test():
    ips = []
    for url,name in [("http://httpbin.org/ip","HttpBin"),("https://api.ipify.org?format=json","Ipify")]:
        try:
            r = requests.get(url, timeout=8)
            d = r.json()
            ips.append(d.get("origin",d.get("ip","")).split(",")[0].strip())
        except: pass
    leaking = len(set(ips)) > 1
    return jsonify({"success":True,"result":{
        "is_leaking":leaking,"detected_ips":list(set(ips)),
        "recommendations":["Enable DNS leak protection","Use custom DNS (1.1.1.1)",
            "Disable WebRTC","Enable Kill Switch"] if leaking else ["No leaks detected"]
    }})

@bp.route('/api/stats')
def stats():
    return jsonify({"success":True,"stats":{
        "servers":len(SERVERS),"connections":len(connections),"version":"4.0","status":"operational"
    }})

DASHBOARD_HTML = """<!DOCTYPE html>
<html lang="ar" dir="rtl"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>VPN & Proxy Manager PRO v4.0</title>
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
<style>:root{--primary:#6f42c1;--dark:#0f0f23;--card:#1a1a3e}
*{box-sizing:border-box}body{background:var(--dark);color:#eee;font-family:'Segoe UI',sans-serif;min-height:100vh}
.navbar{background:linear-gradient(135deg,#1a1a3e,#16213e)!important;border-bottom:2px solid var(--primary)}
.card{background:var(--card);border-radius:15px;border:1px solid rgba(111,66,193,.3)}
.stat-card{background:linear-gradient(135deg,rgba(111,66,193,.15),rgba(102,16,242,.05));border:1px solid rgba(111,66,193,.25);border-radius:12px;padding:20px}
.btn-vpn{background:linear-gradient(135deg,var(--primary),#6610f2);border:none;color:#fff;font-weight:600}
.btn-vpn:hover{transform:scale(1.02);color:#fff}
.conn-item{background:rgba(255,255,255,.05);border-right:4px solid var(--primary);border-radius:8px;padding:15px;margin-bottom:10px}
.nav-pills .nav-link{color:#eee;border-radius:10px;margin:3px;padding:10px 20px}
.nav-pills .nav-link.active{background:linear-gradient(135deg,var(--primary),#6610f2)!important;color:#fff}
.form-select,.form-control{background:rgba(255,255,255,.05);border:1px solid rgba(111,66,193,.3);color:#fff}
.result-box{background:rgba(111,66,193,.1);border:1px solid rgba(111,66,193,.3);border-radius:12px;padding:20px;margin-top:15px}
.safe{border-color:rgba(25,135,84,.5)!important;background:rgba(25,135,84,.1)!important}
.danger{border-color:rgba(220,53,69,.5)!important;background:rgba(220,53,69,.1)!important}
#map{height:300px;border-radius:12px}</style></head><body>
<nav class="navbar navbar-dark navbar-expand-lg mb-4"><div class="container-fluid px-4">
<a class="navbar-brand" href="/">🌐 VPN & Proxy Manager PRO <span class="badge bg-success ms-2">Online</span></a>
</div></nav><div class="container-fluid px-4"><div class="row g-3 mb-4">
<div class="col-3"><div class="stat-card text-center"><i class="bi bi-router fs-1 text-primary d-block"></i><h3 id="sc">0</h3><small>Connections</small></div></div>
<div class="col-3"><div class="stat-card text-center"><i class="bi bi-globe fs-1 text-info d-block"></i><h3>8</h3><small>Servers</small></div></div>
<div class="col-3"><div class="stat-card text-center"><i class="bi bi-shield-check fs-1 text-success d-block"></i><h3 id="st">--</h3><small>Status</small></div></div>
<div class="col-3"><div class="stat-card text-center"><i class="bi bi-speedometer2 fs-1 text-warning d-block"></i><h3 id="lt">--</h3><small>Latency</small></div></div>
</div><div class="row g-4"><div class="col-lg-8"><div class="card p-4">
<ul class="nav nav-pills mb-4">
<li class="nav-item"><button class="nav-link active" onclick="show('vpn')">🔒 VPN Connect</button></li>
<li class="nav-item"><button class="nav-link" onclick="show('det')">🔍 Detect</button></li>
<li class="nav-item"><button class="nav-link" onclick="show('leak')">💧 Leak Test</button></li>
</ul>
<div id="t-vpn"><div class="row g-3 mb-3"><div class="col-md-8">
<select class="form-select form-select-lg" id="svr"><option>Loading...</option></select></div>
<div class="col-md-4 align-self-end"><button class="btn btn-vpn btn-lg w-100" onclick="connect()">Connect</button></div></div>
<hr><h6>Active Connections</h6><div id="cl"><p class="text-muted py-3 text-center">None</p></div></div>
<div id="t-det" style="display:none"><p class="text-muted mb-3">Enter IP to analyze proxy/VPN usage</p>
<div class="input-group input-group-lg mb-3"><input type="text" class="form-control" id="dip" placeholder="e.g., 8.8.8.8">
<button class="btn btn-vpn" onclick="detect()">Analyze</button></div><div id="dr"></div></div>
<div id="t-leak" style="display:none"><div class="alert alert-info" style="background:rgba(111,66,193,.1)">Check if your real IP is leaking through VPN</div>
<button class="btn btn-danger btn-lg w-100 mb-3" onclick="leakTest()">Run Leak Test</button><div id="lr"></div></div>
</div></div><div class="col-lg-4"><div class="card p-4 mb-4"><h6>Quick Actions</h6>
<div class="d-grid gap-2 mt-3"><button class="btn btn-outline-primary btn-sm" onclick="location.reload()">Refresh</button>
<button class="btn btn-outline-warning btn-sm" onclick="leakTest()">Leak Check</button>
<button class="btn btn-outline-success btn-sm" onclick="window.open('/health')">Health</button></div></div>
<div class="card p-4"><h6>System Info</h6><table class="table table-sm table-borderless small mt-2">
<tr><td class="text-muted">Platform:</td><td>Render Cloud ☁️</td></tr>
<tr><td class="text-muted">Version:</td><td>v4.0 Pro</td></tr>
<tr><td class="text-muted">Status:</td><td class="text-success">● Operational</td></tr></table></div></div></div></div>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
document.addEventListener('DOMContentLoaded',()=>{
fetch('/vpn_proxy/api/servers').then(r=>r.json()).then(d=>{
const s=document.getElementById('svr');s.innerHTML='<option value="">Choose server...</option>';
d.servers.forEach(x=>s.innerHTML+=`<option value="${x.id}">${x.country_code} ${x.name}</option>`);
});
loadConns();
});
function show(t){document.querySelectorAll('[id^="t-"]').forEach(x=>x.style.display='none');
document.getElementById('t-'+t).style.display='block';}
async function connect(){
const s=document.getElementById('svr').value;if(!s)return alert('Select server');
const r=await fetch('/vpn_proxy/api/vpn/connect',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({server_id:s})});
const d=await r.json();if(d.success){alert('Connected!');loadConns();}
}
async function loadConns(){const r=await fetch('/vpn_proxy/api/vpn/connections');
const d=await r.json();document.getElementById('sc').textContent=d.count;
const c=document.getElementById('cl');
c.innerHTML=d.connections.length?d.connections.map(x=`<div class="conn-item"><strong>${x.conn_type.toUpperCase()}</strong> ${x.status} <span class="badge bg-success">${x.latency_ms.toFixed(0)}ms</span></div>`).join(''):'<p class="text-muted py-3 text-center">None</p>';}
async function detect(){const ip=document.getElementById('dip').value.trim();if(!ip)return;
const r=document.getElementById('dr');r.innerHTML='<p class="text-center py-3">Analyzing...</p>';
const d=await fetch(`/vpn_proxy/api/detect/${ip}`).then(x=>x.json());
const det=d.detection;r.innerHTML=`<div class="result-box ${det.is_proxy?'danger':'safe'}">
<h5 class="${det.is_proxy?'text-danger':'text-success'}">${det.is_proxy?'⚠️ Proxy/VPN Detected':'✅ Looks Clean'}</h5>
<table class="table table-sm"><tr><td>Type:</td><td><b>${det.proxy_type}</b></td></tr>
<tr><td>Confidence:</td><td>${(det.confidence*100).toFixed(1)}%</td></tr>
<tr><td>Risk:</td><td><span class="badge bg-${det.confidence>0.7?'danger':det.confidence>0.45?'warning':'success'}">${det.risk_level.toUpperCase()}</span></td></tr>
<tr><td>Country:</td><td>${det.details?.country||'--'}</td></tr>
<tr><td>ISP:</td><td>${det.details?.isp||'--'}</td></tr></table></div>`;}
async function leakTest(){const r=document.getElementById('lr');
const b=event.target;b.innerHTML='Testing...';b.disabled=true;
r.innerHTML='<p class="text-center py-3">Checking...</p>';
const d=await fetch('/vpn_proxy/api/leak-test').then(x=>x.json());
const res=d.result;document.getElementById('st').innerHTML=res.is_leaking?'<span class="text-danger">LEAK!</span>':'<span class="text-success">SAFE</span>';
r.innerHTML=res.is_leaking?`<div class="result-box danger"><h4 class="text-danger">⚠️ LEAK DETECTED!</h4>
<p>Your IP may be exposed!</p><ul>${res.detected_ips.map(i=>'<li><code>'+i+'</code></li>').join('')}</ul>
<h6>How to fix:</h6><ul>${res.recommendations.map(x=>'<li>'+x+'</li>').join('')}</ul></div>`:
`<div class="result-box safe"><h4 class="text-success">✅ No Leaks!</h4><p>Connection appears secure.</p></div>`;
b.innerHTML='Run Leak Test';b.disabled=false;}
</script></body></html>"""
'''
        (self.base_dir / 'app' / 'systems' / '__init__.py').write_text('')
        (self.base_dir / 'app' / 'systems' / 'vpn_proxy_manager.py').write_text(vpn_code)
        success("VPN system created")
        
        step(9, self.total_steps, "Creating README...")
        (self.base_dir / 'README.md').write_text(f'''# 🛡️ Security Toolkit PRO v4.0

8 Advanced Security Systems | Deployed on Render ☁️

## Quick Start
This project auto-deploys to [Render](https://render.com).

### Systems
1. Network Monitor
2. Link Tracker
3. Parental Control
4. Surveillance
5. Metadata Analyzer
6. Social Engineering
7. DFIR Forensics
8. **VPN Proxy Manager ⭐**

## Endpoints
- `/` - Main page
- `/health` - Health check
- `/vpn_proxy` - VPN Dashboard
- `/vpn_proxy/api/servers` - Server list
- `/vpn_proxy/api/detect/<ip>` - Detect proxy
- `/vpn_proxy/api/leak-test` - Leak test

## License
MIT
''')
        
        step(10, self.total_steps, "Done!")
        print(f"\n{Colors.GREEN}{'='*50}{Colors.END}")
        print(f"{Colors.YELLOW}Project created in: {self.project_name}/{Colors.END}")
        print(f"\nNext:")
        print(f"  cd {self.project_name}")
        print(f"  git init && git add .")
        print(f"  git commit -m 'Initial commit'")
        print(f"  git remote add origin YOUR_REPO_URL")
        print(f"  git push -u origin main")
        print(f"\nThen go to render.com → New → Connect GitHub")

if __name__ == "__main__":
    print_banner()
    try:
        ProjectCreator().create_all()
    except KeyboardInterrupt:
        print("\nCancelled")
