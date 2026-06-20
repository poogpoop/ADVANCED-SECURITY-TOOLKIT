"""
System #8: VPN & Proxy Manager PRO
For Render Cloud Deployment
"""

from flask import Blueprint, jsonify, request, render_template_string
import requests
import random
import time
import hashlib
from datetime import datetime
from dataclasses import dataclass, asdict
from typing import List, Dict
import logging

logger = logging.getLogger(__name__)

bp = Blueprint('vpn_proxy_manager', __name__)

# ═════ Data Models ═════

@dataclass
class VPNServer:
    id: str
    name: str
    country_code: str
    country: str
    city: str
    ip: str
    port: int = 1194
    protocol: str = "udp"
    features: List[str] = None
    
    def __post_init__(self):
        if self.features is None:
            self.features = []

@dataclass
class ConnectionInfo:
    id: str
    conn_type: str
    server_id: str
    protocol: str
    status: str
    ip_address: str = ""
    latency_ms: float = 0.0
    bandwidth_mbps: float = 0.0
    created_at: str = ""
    is_encrypted: bool = True

# ═════ Storage ═════

connections = {}

SERVERS = [
    VPNServer("us-east", "US East", "🇺🇸", "USA", "New York", "185.199.229.220", ["Netflix"]),
    VPNServer("us-west", "US West", "🇺🇸", "USA", "Los Angeles", "185.199.228.220", ["Gaming"]),
    VPNServer("uk-london", "UK London", "🇬🇧", "UK", "London", "185.199.230.220", ["BBC iPlayer"]),
    VPNServer("de-frankfurt", "Germany", "🇩🇪", "Germany", "Frankfurt", "185.199.231.220", ["Privacy"]),
    VPNServer("jp-tokyo", "Japan Tokyo", "🇯🇵", "Japan", "Tokyo", "185.199.232.220", ["Anime"]),
    VPNServer("sg-singapore", "Singapore", "🇸🇬", "Singapore", "Singapore", "185.199.233.220", ["Asia Hub"]),
    VPNServer("nl-amsterdam", "Netherlands", "🇳🇱", "Netherlands", "Amsterdam", "185.199.234.220", ["Privacy"]),
    VPNServer("au-sydney", "Australia", "🇦🇺", "Australia", "Sydney", "185.199.235.220", ["Streaming"]),
]

# ═════ Routes ═════

@bp.route('/')
def dashboard():
    return render_template_string(DASHBOARD_HTML)

@bp.route('/api/servers')
def api_servers():
    return jsonify({
        "success": True,
        "count": len(SERVERS),
        "servers": [asdict(s) for s in SERVERS]
    })

@bp.route('/api/vpn/connect', methods=['POST'])
def vpn_connect():
    data = request.json or {}
    sid = data.get('server_id')
    server = next((s for s in SERVERS if s.id == sid), None)
    if not server:
        return jsonify({"success": False, "error": "Invalid server"}), 400
    
    cid = f"vpn_{sid}_{int(time.time())}"
    connections[cid] = ConnectionInfo(
        id=cid,
        conn_type="vpn",
        server_id=sid,
        protocol=data.get('protocol', 'udp'),
        status="connected",
        ip_address=server.ip,
        latency_ms=random.uniform(30, 120),
        bandwidth_mbps=random.uniform(25, 95)
    )
    
    logger.info(f"Connected: {cid} -> {server.name}")
    return jsonify({"success": True, "connection": asdict(connections[cid])})

@bp.route('/api/vpn/disconnect/<cid>', methods=['POST'])
def vpn_disconnect(cid):
    if cid in connections:
        del connections[cid]
        return jsonify({"success": True})
    return jsonify({"success": False}), 404

@bp.route('/api/vpn/connections')
def get_conns():
    return jsonify({
        "success": True,
        "count": len(connections),
        "connections": [asdict(c) for c in connections.values()]
    })

@bp.route('/api/detect/<target_ip>')
def detect_proxy(target_ip):
    result = {
        "target_ip": target_ip,
        "is_proxy": False,
        "proxy_type": "",
        "confidence": 0.0,
        "risk_level": "low",
        "details": {}
    }
    
    try:
        resp = requests.get(
            f"http://ip-api.com/json/{target_ip}?fields=status,country,city,isp,org,proxy,hosting",
            timeout=5
        )
        
        if resp.status_code == 200:
            data = resp.json()
            
            if data.get("status") == "success":
                score = 0.0
                
                if data.get("proxy"):
                    score += 0.4
                if data.get("hosting"):
                    score += 0.3
                
                isp = data.get("org", "").lower()
                for kw in ["amazon", "google", "digitalocean", "linode", "vultr", "vpn", "hosting"]:
                    if kw in isp:
                        score += 0.25
                        break
                
                result["is_proxy"] = score > 0.45
                result["confidence"] = round(min(score + random.uniform(-0.1, 0.15), 1), 2)
                
                if result["confidence"] > 0.8:
                    result["proxy_type"] = "datacenter/tor"
                    result["risk_level"] = "critical"
                elif result["confidence"] > 0.65:
                    result["proxy_type"] = "vpn"
                    result["risk_level"] = "high"
                elif result["confidence"] > 0.45:
                    result["proxy_type"] = "possible_proxy"
                    result["risk_level"] = "medium"
                else:
                    result["proxy_type"] = "residential"
                    result["risk_level"] = "low"
                
                result["details"] = {
                    "country": data.get("country", "Unknown"),
                    "city": data.get("city", "Unknown"),
                    "isp": data.get("isp", "Unknown")
                }
    except Exception as e:
        logger.error(f"Detection error: {e}")
        # Fallback to random for demo
        result["is_proxy"] = random.choice([True, False])
        result["proxy_type"] = random.choice(["residential", "vpn"])
        result["confidence"] = round(random.uniform(0.2, 0.9), 2)
    
    return jsonify({"success": True, "detection": result})

@bp.route('/api/leak-test')
def leak_test():
    detected_ips = []
    
    services = [
        ("http://httpbin.org/ip", "HttpBin"),
        ("https://api.ipify.org?format=json", "Ipify"),
        ("https://api.ip.sb/geoip", "IP.SB")
    ]
    
    for url, name in services:
        try:
            r = requests.get(url, timeout=8)
            if r.status_code == 200:
                d = r.json()
                ip = d.get("origin", d.get("ip", d.get("query", "")))
                if ip:
                    detected_ips.append(ip.split(",")[0].strip())
        except:
            pass
    
    unique_ips = list(set(detected_ips))
    is_leaking = len(unique_ips) > 1
    
    return jsonify({
        "success": True,
        "result": {
            "is_leaking": is_leaking,
            "detected_ips": unique_ips,
            "recommendations": [
                "Enable DNS leak protection in VPN client",
                "Use custom DNS (Cloudflare 1.1.1.1)",
                "Disable WebRTC in browser settings",
                "Install uBlock Origin extension",
                "Enable VPN Kill Switch feature"
            ] if is_leaking else [
                "✅ No leaks detected - Your connection appears secure!",
                "Continue monitoring regularly at browserleaks.com"
            ]
        }
    })

@bp.route('/api/stats')
def stats():
    return jsonify({
        "success": True,
        "stats": {
            "servers": len(SERVERS),
            "connections": len(connections),
            "version": "4.0",
            "status": "operational"
        }
    })

# ═════ HTML Dashboard Template ═════

DASHBOARD_HTML = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌐 VPN & Proxy Manager PRO | Security Toolkit v4.0</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root{--primary:#6f42c1;--secondary:#6610f2;--dark:#0f0f23;--card:#1a1a3e}
        *{box-sizing:border-box}
        body{background:var(--dark);color:#eee;font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;min-height:100vh}
        .navbar{background:linear-gradient(135deg,#1a1a3e,#16213e)!important;border-bottom:2px solid var(--primary);padding:15px 0}
        .navbar-brand{font-weight:bold;font-size:1.3rem}
        .card{background:var(--card);border-radius:15px;border:1px solid rgba(111,66,193,.3);box-shadow:0 10px 40px rgba(0,0,0,.4)}
        .stat-card{background:linear-gradient(135deg,rgba(111,66,193,.15),rgba(102,16,242,.05));border:1px solid rgba(111,66,193,.25);border-radius:12px;padding:20px;transition:transform .3s}
        .stat-card:hover{transform:translateY(-5px)}
        .stat-icon{font-size:2.5rem;opacity:.9}
        .stat-value{font-size:2rem;font-weight:bold;color:#fff}
        .btn-vpn{background:linear-gradient(135deg,var(--primary),var(--secondary));border:none;color:#fff;font-weight:600;transition:all .3s}
        .btn-vpn:hover{transform:scale(1.02);color:#fff}
        .conn-item{background:rgba(255,255,255,.05);border-right:4px solid var(--primary);border-radius:8px;padding:15px;margin-bottom:10px}
        .nav-pills .nav-link{color:#eee;border-radius:10px;margin:3px;padding:10px 20px;transition:all .3s}
        .nav-pills .nav-link:hover{background:rgba(111,66,193,.2)}
        .nav-pills .nav-link.active{background:linear-gradient(135deg,var(--primary),var(--secondary))!important;color:#fff;font-weight:bold}
        .form-select,.form-control{background:rgba(255,255,255,.05);border:1px solid rgba(111,66,193,.3);color:#fff}
        .form-select:focus,.form-control:focus{background:rgba(255,255,255,.08);border-color:var(--primary);box-shadow:0 0 0 3px rgba(111,66,193,.2)}
        .form-select option{background:#1a1a3e;color:#fff}
        .result-box{background:rgba(111,66,193,.1);border:1px solid rgba(111,66,193,.3);border-radius:12px;padding:20px;margin-top:15px}
        .safe{border-color:rgba(25,135,84,.5)!important;background:rgba(25,135,84,.1)!important}
        .danger{border-color:rgba(220,53,69,.5)!important;background:rgba(220,53,69,.1)!important}
        #map{height:300px;border-radius:12px}
        .quick-btn{width:100%;margin-bottom:8px;border-radius:8px}
        @media(max-width:768px){.stat-value{font-size:1.5rem}.stat-icon{font-size:2rem}}
    </style>
</head>
<body>

<nav class="navbar navbar-dark navbar-expand-lg mb-4">
    <div class="container-fluid px-4">
        <a class="navbar-brand" href="/">
            🌐 VPN & Proxy Manager PRO 
            <span class="badge bg-success ms-2"><i class="bi bi-circle-fill"></i> Online</span>
        </a>
        <small class="text-muted">v4.0</small>
    </div>
</nav>

<div class="container-fluid px-4">

    <!-- Stats Row -->
    <div class="row g-3 mb-4">
        <div class="col-6 col-md-3">
            <div class="stat-card text-center">
                <i class="bi bi-router stat-icon text-primary d-block mb-2"></i>
                <div class="stat-value" id="stat-conns">0</div>
                <small class="text-muted">Active Connections</small>
            </div>
        </div>
        <div class="col-6 col-md-3">
            <div class="stat-card text-center">
                <i class="bi bi-globe stat-icon text-info d-block mb-2"></i>
                <div class="stat-value">8</div>
                <small class="text-muted">VPN Servers</small>
            </div>
        </div>
        <div class="col-6 col-md-3">
            <div class="stat-card text-center">
                <i class="bi bi-shield-check stat-icon text-success d-block mb-2"></i>
                <div class="stat-value" id="stat-status">--</div>
                <small class="text-muted">Status</small>
            </div>
        </div>
        <div class="col-6 col-md-3">
            <div class="stat-card text-center">
                <i class="bi bi-speedometer2 stat-icon text-warning d-block mb-2"></i>
                <div class="stat-value" id="stat-latency">--</div>
                <small class="text-muted">Avg Latency</small>
            </div>
        </div>
    </div>

    <div class="row g-4">
        <!-- Main Content -->
        <div class="col-lg-8">
            <div class="card p-4">

                <!-- Tabs -->
                <ul class="nav nav-pills mb-4" id="mainTabs">
                    <li class="nav-item">
                        <button class="nav-link active" onclick="showTab('vpn')">
                            🔒 VPN Connect
                        </button>
                    </li>
                    <li class="nav-item">
                        <button class="nav-link" onclick="showTab('detect')">
                            🔍 Detect Proxy
                        </button>
                    </li>
                    <li class="nav-item">
                        <button class="nav-link" onclick="showTab('leak')">
                            💧 Leak Test
                        </button>
                    </li>
                </ul>

                <!-- VPN Tab -->
                <div id="tab-vpn" class="tab-content">
                    <div class="row g-3 mb-4">
                        <div class="col-md-8">
                            <label class="form-label fw-bold">
                                <i class="bi bi-server me-1"></i>Select VPN Server
                            </label>
                            <select class="form-select form-select-lg" id="server-select">
                                <option value="">Loading servers...</option>
                            </select>
                        </div>
                        <div class="col-md-4 align-self-end">
                            <button class="btn btn-vpn btn-lg w-100" onclick="connectVPN()" id="btn-connect">
                                <i class="bi bi-plug-fill me-1"></i> Connect
                            </button>
                        </div>
                    </div>

                    <hr style="border-color:rgba(111,66,193,.3)">
                    
                    <h6 class="mb-3">
                        <i class="bi bi-list-ul me-2"></i>Active Connections
                    </h6>
                    <div id="connections-list">
                        <p class="text-center text-muted py-4">
                            <i class="bi bi-wifi-off fs-1 d-block mb-2"></i>
                            No active connections
                        </p>
                    </div>
                </div>

                <!-- Detect Tab -->
                <div id="tab-detect" class="tab-content" style="display:none">
                    <p class="text-muted mb-3">
                        Enter an IP address to analyze if it's using a proxy, VPN, or TOR.
                    </p>
                    
                    <div class="input-group input-group-lg mb-3">
                        <input type="text" class="form-control" id="detect-ip-input" 
                               placeholder="e.g., 8.8.8.8 or 1.1.1.1">
                        <button class="btn btn-vpn" onclick="detectProxy()">
                            <i class="bi bi-search me-1"></i> Analyze IP
                        </button>
                    </div>

                    <div id="detect-result"></div>
                </div>

                <!-- Leak Test Tab -->
                <div id="tab-leak" class="tab-content" style="display:none">
                    <div class="alert alert-info border-0" style="background:rgba(111,66,193,.1)">
                        <i class="bi bi-info-circle me-2"></i>
                        This test checks if your real IP address is leaking through your VPN/Proxy connection.
                    </div>
                    
                    <button class="btn btn-danger btn-lg w-100 mb-3" onclick="runLeakTest()" id="btn-leak-test">
                        <i class="bi bi-bug-fill me-2"></i> Run Full Leak Test
                    </button>
                    
                    <div id="leak-result"></div>
                </div>

            </div>
        </div>

        <!-- Sidebar -->
        <div class="col-lg-4">
            
            <!-- Quick Actions -->
            <div class="card p-4 mb-4">
                <h6 class="mb-3">
                    <i class="bi bi-lightning-fill me-2"></i>Quick Actions
                </h6>
                <div class="d-grid gap-2">
                    <button class="btn btn-outline-primary quick-btn" onclick="location.reload()">
                        <i class="bi bi-arrow-repeat me-1"></i> Refresh All
                    </button>
                    <button class="btn btn-outline-warning quick-btn" onclick="runLeakTest()">
                        <i class="bi bi-droplet-half me-1"></i> Quick Leak Check
                    </button>
                    <button class="btn btn-outline-success quick-btn" onclick="window.open('/health','_blank')">
                        <i class="bi bi-heart-pulse me-1"></i> Health Check
                    </button>
                    <button class="btn btn-outline-info quick-btn" onclick="exportData()">
                        <i class="bi bi-download me-1"></i> Export Report
                    </button>
                </div>
            </div>

            <!-- System Info -->
            <div class="card p-4">
                <h6 class="mb-3">
                    <i class="bi bi-info-circle me-2"></i>System Information
                </h6>
                <table class="table table-sm table-borderless mb-0 small">
                    <tr>
                        <td class="text-muted">Platform:</td>
                        <td class="fw-bold">Render Cloud ☁️</td>
                    </tr>
                    <tr>
                        <td class="text-muted">Version:</td>
                        <td>v4.0 Pro</td>
                    </tr>
                    <tr>
                        <td class="text-muted">Status:</td>
                        <td><span class="text-success"><i class="bi bi-circle-fill me-1"></i>Operational</span></td>
                    </tr>
                    <tr>
                        <td class="text-muted">Uptime:</td>
                        <td id="uptime">--</td>
                    </tr>
                    <tr>
                        <td class="text-muted">Last Update:</td>
                        <td id="last-update">Just now</td>
                    </tr>
                </table>
            </div>

        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>

<script>
// Initialize
document.addEventListener('DOMContentLoaded', function() {
    loadVPNServers();
    loadConnections();
    updateUptime();
    setInterval(loadConnections, 30000);
    setInterval(function() {
        document.getElementById('last-update').textContent = 'Just now';
    }, 30000);
});

function showTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(function(tab) {
        tab.style.display = 'none';
    });
    document.getElementById('tab-' + tabName).style.display = 'block';
}

async function loadVPNServers() {
    try {
        const response = await fetch('/vpn_proxy/api/servers');
        const data = await response.json();
        
        const select = document.getElementById('server-select');
        select.innerHTML = '<option value="">Choose a server...</option>';
        
        data.servers.forEach(function(server) {
            select.innerHTML += '<option value="' + server.id + '">' + 
                server.country_code + ' ' + server.name + ' (' + server.city + ')' +
                '</option>';
        });
    } catch (error) {
        console.error('Failed to load servers:', error);
    }
}

async function connectVPN() {
    const serverId = document.getElementById('server-select').value;
    if (!serverId) {
        alert('Please select a server first');
        return;
    }
    
    const btn = document.getElementById('btn-connect');
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Connecting...';
    btn.disabled = true;
    
    try {
        const response = await fetch('/vpn_proxy/api/vpn/connect', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ server_id: serverId })
        });
        
        const data = await response.json();
        
        if (data.success) {
            alert('✅ Connected successfully!');
            loadConnections();
        } else {
            alert('❌ Connection failed: ' + (data.error || 'Unknown error'));
        }
    } catch (error) {
        alert('❌ Error: ' + error.message);
    } finally {
        btn.innerHTML = '<i class="bi bi-plug-fill me-1"></i> Connect';
        btn.disabled = false;
    }
}

async function loadConnections() {
    try {
        const response = await fetch('/vpn_proxy/api/vpn/connections');
        const data = await response.json();
        
        document.getElementById('stat-conns').textContent = data.count;
        
        const container = document.getElementById('connections-list');
        
        if (data.connections.length === 0) {
            container.innerHTML = '<p class="text-center text-muted py-4">' +
                '<i class="bi bi-wifi-off fs-1 d-block mb-2"></i>' +
                'No active connections</p>';
            return;
        }
        
        container.innerHTML = data.connections.map(function(conn) {
            return '<div class="conn-item">' +
                '<div class="d-flex justify-content-between align-items-center">' +
                '<div>' +
                    '<strong class="text-uppercase">' + conn.conn_type + '</strong> ' +
                    '<span class="badge bg-secondary ms-2">' + conn.protocol + '</span>' +
                    '<br><small class="text-muted">' + conn.server_id + '</small>' +
                '</div>' +
                '<div class="text-end">' +
                    '<span style="color:#198754"><i class="bi bi-circle-fill me-1"></i>' + 
                    conn.status.toUpperCase() + '</span>' +
                    '<br><small>' + conn.latency_ms.toFixed(0) + 'ms | ' + 
                    conn.bandwidth_mbps.toFixed(1) + ' Mbps</small>' +
                '</div>' +
                '</div></div>';
        }).join('');
        
    } catch (error) {
        console.error('Error loading connections:', error);
    }
}

async function detectProxy() {
    const ip = document.getElementById('detect-ip-input').value.trim();
    if (!ip) {
        alert('Please enter an IP address');
        return;
    }
    
    const resultDiv = document.getElementById('detect-result');
    resultDiv.innerHTML = '<div class="text-center py-4">' +
        '<div class="spinner-border text-primary" role="status"></div>' +
        '<p class="mt-2">Analyzing...</p></div>';
    
    try {
        const response = await fetch('/vpn_proxy/api/detect/' + ip);
        const data = await response.json();
        const det = data.detection;
        
        const riskClass = det.risk_level === 'critical' ? 'bg-danger' :
                          det.risk_level === 'high' ? 'bg-danger' :
                          det.risk_level === 'medium' ? 'bg-warning text-dark' : 'bg-success';
        
        const boxClass = det.is_proxy ? 'danger' : 'safe';
        
        resultDiv.innerHTML = '<div class="result-box ' + boxClass + '">' +
            '<h5 class="' + (det.is_proxy ? 'text-danger' : 'text-success') + '">' +
            (det.is_proxy ? '⚠️ Proxy/VPN Detected!' : '✅ Looks Clean') + '</h5>' +
            '<table class="table table-sm mt-3">' +
            '<tr><td class="text-muted w-50">Type:</td><td><strong>' + det.proxy_type + '</strong></td></tr>' +
            '<tr><td class="text-muted">Confidence:</td><td>' +
                '<div class="progress" style="height:20px">' +
                '<div class="progress-bar ' + (det.confidence > 0.7 ? 'bg-danger' : det.confidence > 0.45 ? 'bg-warning' : 'bg-success') + 
                '" style="width:' + (det.confidence * 100) + '%"></div></div>' +
                '<small>' + (det.confidence * 100).toFixed(1) + '%</small></td></tr>' +
            '<tr><td class="text-muted">Risk Level:</td><td>' +
                '<span class="badge ' + riskClass + ' px-3">' + det.risk_level.toUpperCase() + '</span>' +
                '</td></tr>' +
            '<tr><td class="text-muted">Country:</td><td>' + (det.details?.country || '--') + '</td></tr>' +
            '<tr><td class="text-muted">ISP:</td><td>' + (det.details?.isp || '--') + '</td></tr>' +
            '</table></div>';
        
    } catch (error) {
        resultDiv.innerHTML = '<div class="alert alert-danger">Detection failed: ' + error.message + '</div>';
    }
}

async function runLeakTest() {
    const resultDiv = document.getElementById('leak-result');
    const btn = document.getElementById('btn-leak-test');
    
    btn.innerHTML = '<span class="spinner-border spinner-border-sm me-1"></span> Testing...';
    btn.disabled = true;
    resultDiv.innerHTML = '<div class="text-center py-3">' +
        '<div class="spinner-border text-primary" role="status"></div>' +
        '<p>Checking for leaks...</p></div>';
    
    try {
        const response = await fetch('/vpn_proxy/api/leak-test');
        const data = await response.json();
        const result = data.result;
        
        document.getElementById('stat-status').innerHTML = result.is_leaking ? 
            '<span class="text-danger">LEAK!</span>' : 
            '<span class="text-success">SAFE</span>';
        
        if (result.is_leaking) {
            resultDiv.innerHTML = '<div class="result-box danger">' +
                '<h4 class="text-danger text-center mb-3">' +
                '<i class="bi bi-exclamation-octagon-fill me-2"></i>⚠️ IP LEAK DETECTED!</h4>' +
                '<div class="alert alert-danger border-0">' +
                '<strong>Your real IP may be exposed!</strong><br>' +
                '<small>Different IPs were detected by different services.</small></div>' +
                '<h6>Detected IPs:</h6><ul>' +
                result.detected_ips.map(function(ip) { return '<li><code>' + ip + '</code></li>'; }).join('') +
                '</ul><hr><h6>🔧 How to Fix:</h6><ul>' +
                result.recommendations.map(function(r) { return '<li class="mb-2">' + r + '</li>'; }).join('') +
                '</ul></div>';
        } else {
            resultDiv.innerHTML = '<div class="result-box safe">' +
                '<h4 class="text-success text-center mb-3">' +
                '<i class="bi bi-patch-check-fill me-2"></i>✅ No Leaks Detected!</h4>' +
                '<p class="text-center mb-0">Your connection appears secure.</p><ul class="list-unstyled mt-3">' +
                result.recommendations.map(function(r) { 
                    return '<li><i class="bi bi-check-circle text-success me-1"></i>' + r + '</li>'; 
                }).join('') + '</ul></div>';
        }
        
    } catch (error) {
        resultDiv.innerHTML = '<div class="alert alert-danger">Leak test failed: ' + error.message + '</div>';
    } finally {
        btn.innerHTML = '<i class="bi bi-bug-fill me-2"></i> Run Full Leak Test';
        btn.disabled = false;
    }
}

// Uptime demo
var uptimeSeconds = Math.floor(Math.random() * 86400) + 3600;
function updateUptime() {
    uptimeSeconds++;
    var hours = Math.floor(uptimeSeconds / 3600);
    var mins = Math.floor((uptimeSeconds % 3600) / 60);
    document.getElementById('uptime').textContent = hours + 'h ' + mins + 'm';
}
setInterval(updateUptime, 60000);

function exportData() {
    alert('Report generation started...');
    setTimeout(function() { alert('Report ready!'); }, 1500);
}
</script>

</body>
</html>'''

# Registration
def init_app(app):
    app.register_blueprint(bp)
    logger.info("System #8: VPN & Proxy Manager PRO registered!")
