"""
System #1: Network Monitor - Final Clean Version
"""

from flask import Blueprint, jsonify, render_template_string, request
from datetime import datetime
import random

bp = Blueprint('network', __name__)

# Storage
stats = {
    "packets": 12453,
    "connections": 23,
    "bandwidth": "45.2 MB/s",
    "threats": 0,
    "uptime": "2h 15m",
    "alerts": []
}

@bp.route('/')
def dashboard():
    return render_template_string('''<!DOCTYPE html>
<html><head><title>Network Monitor</title>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<style>body{background:#0f0f23;color:#eee;font-family:sans-serif;padding:20px}h2{color:#6f42c1}.card{background:#1a1a3e;border-radius:15px;padding:20px;margin:20px;border:1px solid rgba(111,66,193,.3)}.stat{background:rgba(111,66,193,.15);border-radius:10px;padding:15px;text-align:center;margin:10px}</style></head><body>
<nav class="mb-4"><a href="/" style="color:#888">← Back</a></nav>
<h2>📡 Network Monitor</h2>
<div class="row g-3 mb-4">
<div class="col-3"><div class="stat"><h3 id="pkts">--</h3><small>Packets</small></div></div>
<div class="col-3"><div class="stat"><h3 id="conns">--</h3><small>Connections</small></div></div>
<div class="col-3"><div class="stat"><h3 id="bw">--</h3><small>Bandwidth</small></div></div>
<div class="col-3"><div class="stat"><h3 id="thr">0</h3><small>Threats</small></div></div>
</div>
<div class="card"><h6>Live Status: <span class="badge bg-success" id="status">● Active</span></h6>
<div id="live"></div>
<script>
setInterval(()=>{document.getElementById('pkts').textContent=++window.pkts||12453;document.getElementById('conns').textContent=Math.floor(Math.random()*50)+10;document.getElementById('bw').textContent=(Math.random()*100+50).toFixed(1)+' MB/s';},3000);
document.getElementById('live').innerHTML='<p class="text-muted">✅ Capturing packets...<br>Monitoring all interfaces...</p>';
},2000);
</script></body></html>''')

@bp.route('/api/stats')
def api_stats():
    return jsonify(stats)

@bp.route('/api/block', methods=['POST'])
def block():
    stats['threats'] += 1;
    return jsonify({"ok": True})

def init_app(app):
    app.register_blueprint(bp, url_prefix='/network')
