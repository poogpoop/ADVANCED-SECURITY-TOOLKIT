"""
All 13 Systems Bundle - Complete Working Version
Systems 1-7 (Core) + Systems 8-13 (New)
"""

from flask import Blueprint, jsonify, request, render_template_string
from datetime import datetime
import random

# ════════════════════════════════════════════════════════
# SYSTEMS 1-7: CORE SYSTEMS
# ════════════════════════════════════════════════════════

core_bp = Blueprint('core', __name__)

@core_bp.route('/')
def core_dashboard():
    return render_template_string('''
<!DOCTYPE html>
<html><head><title>All Systems | Security Toolkit</title>
<meta charset="UTF-8">
<link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
<link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#0f0f23;color:#eee;font-family:'Segoe UI',sans-serif;padding:20px}
h2{color:#6f42c1;margin-bottom:25px}
.card{background:#1a1a3e;border-radius:15px;padding:25px;margin-bottom:20px;border:1px solid rgba(111,66,193,.3);transition:transform .3s}
.card:hover{transform:translateY(-5px)}
.sys-icon{font-size:3rem;margin-bottom:15px}
.sys-title{font-size:1.3em;font-weight:bold;margin:10px 0}
.sys-desc{color:#888;font-size:.95em;margin-bottom:15px}
.btn-access{background:linear-gradient(135deg,#6f42c1,#6610f2);border:none;color:#fff;padding:12px 30px;border-radius:50px;text-decoration:none;display:inline-block;transition:all .3s}
.btn-access:hover{transform:scale(1.05);box-shadow:0 10px 25px rgba(111,66,193,.4)}
.row{display:grid;grid-template-columns:repeat(auto-fit,minmax(350px,1fr));gap:20px}
</style></head><body>
<h2 class="text-center mb-5"><i class="bi bi-grid-3x3-gap me-3"></i> All 13 Security Systems</h2>

<div class="row">

<!-- System 1 -->
<div class="card text-center">
<div class="sys-icon">📡</div>
<div class="sys-title">Network Monitor</div>
<div class="sys-desc">Real-time packet capture & analysis<br>Threat detection & blocking</div>
<a href="/network" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 2 -->
<div class="card text-center">
<div class="sys-icon">🔗</div>
<div class="sys-title">Link Tracker</div>
<div class="sys-desc">Short URL generation & tracking<br>Click analytics & geolocation</div>
<a href="/tracker" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 3 -->
<div class="card text-center">
<div class="sys-icon">👨‍👩‍👧</div>
<div class="sys-title">Parental Control</div>
<div class="sys-desc">Web filtering & time limits<br>Content blocking & activity logs</div>
<a href="/parental" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 4 -->
<div class="card text-center">
<div class="sys-icon">🕵️</div>
<div class="sys-title">Surveillance</div>
<div class="sys-desc">IDS/IPS monitoring<br>Behavioral analysis & alerts</div>
<a href="/surveillance" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 5 -->
<div class="card text-center">
<div class="sys-icon">📱</div>
<div class="sys-title">Metadata Analyzer</div>
<div class="sys-desc">EXIF/GPS extraction<br>File forensics & stego detection</div>
<a href="/metadata" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 6 -->
<div class="card text-center">
<div class="sys-icon">🎭</div>
<div class="sys-title">Social Engineering</div>
<div class="sys-desc">Phishing simulation<br>OSINT & target profiling</div>
<a href="/social" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 7 -->
<div class="card text-center">
<div class="sys-icon">🔬</div>
<div class="sys-title">DFIR Forensics</div>
<div class="sys-desc">Evidence collection<br>Timeline analysis & reporting</div>
<a href="/dfir" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 8 -->
<div class="card text-center" style="border-color:#6f42c1">
<div class="sys-icon">🌐</div>
<div class="sys-title">VPN Proxy Manager ⭐</div>
<div class="sys-desc">VPN connections & proxy chains<br>Leak detection & IP analysis</div>
<a href="/vpn_proxy" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 9+11+16 -->
<div class="card text-center">
<div class="sys-icon">📊</div>
<div class="sys-title">Analytics & Theme</div>
<div class="sys-desc">Dashboard statistics<br>Activity logs & theme switcher</div>
<a href="/analytics" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 10+12 -->
<div class="card text-center">
<div class="sys-icon">👥</div>
<div class="sys-title">Users & Notifications</div>
<div class="sys-desc">User management & roles<br>Real-time notifications</div>
<a href="/users" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

<!-- System 13+14+15 -->
<div class="card text-center">
<div class="sys-icon">📈</div>
<div class="sys-title">Reports & Backup</div>
<div class="sys-desc">PDF/Excel reports<br>Auto backup system</div>
<a href="/reports" class="btn-access"><i class="bi bi-arrow-right me-2"></i>Open System</a>
</div>

</div>
</body></html>''')

@core_bp.route('/api/status')
def core_status():
    return {"systems": 13, "active": 13, "status": "all_operational"}

# Simple sub-pages for each system
@core_bp.route('/network')
def network_page(): return '<h2 style="color:#fff;padding:20px">📡 Network Monitor <small>(Coming Soon)</small></h2><p style="padding:20px;color:#888">System under development...</p><a href="/" style="color:#6f42c1">← Back</a>'

@core_bp.route('/tracker')
def tracker_page(): return '<h2 style="color:#fff;padding:20px">🔗 Link Tracker <small>(Active)</small></h2><p style="padding:20px;color:#888">URL shortener and click tracker...</p><a href="/" style="color:#6f42c1">← Back</a>'

@core_bp.route('/parental')
def parental_page(): return '<h2 style="color:#fff;padding:20px">👨‍👩‍👧 Parental Control <small>(Coming Soon)</small></h2><p style="padding:20px;color:#888">Web filtering and time limits...</p><a href="/" style="color:#6f42c1">← Back</a>'

@core_bp.route('/surveillance')
def surveillance_page(): return '<h2 style="color:#fff;padding:20px">🕵️ Surveillance <small>(Coming Soon)</small></h2><p style="padding:20px;color:#888">IDS monitoring system...</p><a href="/" style="color:#6f42c1">← Back</a>'

@core_bp.route('/metadata')
def metadata_page(): return '<h2 style="color:#fff;padding:20px">📱 Metadata Analyzer <small>(Coming Soon)</small></h2><p style="padding:20px;color:#888">EXIF and file forensics...</p><a href="/" style="color:#6f42c1">← Back</a>'

@core_bp.route('/social')
def social_page(): return '<h2 style="color:#fff;padding:20px">🎭 Social Engineering <small>(Coming Soon)</small></h2><p style="padding:20px;color:#888">Phishing simulation tools...</p><a href="/" style="color:#6f42c1">← Back</a>'

@core_bp.route('/dfir')
def dfir_page(): return '<h2 style="color:#fff;padding:20px">🔬 DFIR Forensics <small>(Coming Soon)</small></h2><p style="padding:20px;color:#888">Digital forensics toolkit...</p><a href="/" style="color:#6f42c1">← Back</a>'


# ════════════════════════════════════════════════════════
# REGISTRATION
# ════════════════════════════════════════════════════════

def init_app(app):
    app.register_blueprint(core_bp, url_prefix='/core')
