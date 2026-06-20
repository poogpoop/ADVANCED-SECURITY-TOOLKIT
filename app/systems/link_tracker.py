from flask import Blueprint, jsonify, request, render_template_string
from datetime import datetime
import random
import string
import hashlib

bp = Blueprint('tracker', __name__)

links_db = []

@bp.route('/')
def tracker_dashboard():
    return render_template_string('''<!DOCTYPE html><html><head><title>🔗 Link Tracker</title>
<meta charset="UTF-8"><link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet"><style>body{background:#0f0f23;color:#eee;font-family:sans-serif;padding:20px}h2{color:#6f42c1}.card{background:#1a1a3e;border-radius:15px;padding:20px;margin:20px;border:1px solid rgba(111,66,193,.3)}.input-group{margin:15px 0}.btn{background:linear-gradient(135deg,#6f42c1,#6610f2);border:none;color:#fff;padding:12px 30px;border-radius:25px}.item{background:rgba(255,255,255,.03);padding:12px;border-radius:8px;margin:8px;display:flex;justify-content:space-between;align-items:center}</style></head><body><nav class="mb-4"><a href="/" style="color:#888">← Back</a></nav><h2>🔗 Link Tracker</h2><div class="card"><h6>Create Short Link</h6><div class="input-group"><input type="text" class="form-control" id="urlInput" placeholder="Enter URL to shorten..."><button class="btn btn-primary" onclick="createLink()">Shorten</button></div></div><h6>Your Links (<span id="count">0</span>)</h6><div id="links"></div><script>function loadLinks(){fetch('/tracker/api/links').then(r=>r.json()).then(d=>{document.getElementById("count").textContent=d.length;document.getElementById("links").innerHTML=d.map(l=`
'<div class="item"><strong>/go/'+l.short_code+'</strong><span class="badge bg-primary">'+l.clicks+' clicks</span><span class="badge '+("bg-success" if l.status=="active" else "bg-secondary")+'">'+l.status+'</span></div>').join('')});}async function createLink(){const u=document.getElementById("urlInput").value;if(!u)return alert("Enter URL");const r=await fetch("/tracker/api/create",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({url:u})});document.getElementById("urlInput").value="";loadLinks();}</script></body></html>''')

@bp.route('/api/links')
def tracker_links(): return jsonify(links_db)

@bp.route('/api/create', methods=['POST'])
def tracker_create():
    data = request.json or {}
    new_link = {
        "id": len(links_db)+1,
        "short_code": ''.join(random.choices(string.ascii_letters + string.digits, k=6)),
        "original_url": data.get("url",""),
        "clicks": 0,
        "created": datetime.now().strftime("%Y-%m-%d"),
        "status": "active"
    }
    links_db.insert(0,new_link)
    return jsonify({"success":True,"link":new_link})

def init_app(app):
    app.register_blueprint(bp, url_prefix='/tracker')
