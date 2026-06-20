"""
System #9: Dashboard Analytics
System #11: Activity Log  
System #16: Theme Switcher
"""

from flask import Blueprint, jsonify, request, render_template_string
from datetime import datetime, timedelta
import random
import json

bp = Blueprint('analytics', __name__)

# ═══════ In-Memory Storage ═════

# Analytics Data
analytics_data = {
    "total_visits": random.randint(500, 2000),
    "unique_visitors": random.randint(100, 500),
    "active_connections": 0,
    "requests_today": random.randint(50, 300),
    "avg_response_time": round(random.uniform(20, 150), 1),
    "uptime_percentage": 99.9,
    "systems_status": {
        "network_monitor": {"status": "online", "uptime": "99.9%", "last_check": "2 min ago"},
        "link_tracker": {"status": "online", "uptime": "99.8%", "last_check": "1 min ago"},
        "parental_control": {"status": "online", "uptime": "100%", "last_check": "30 sec ago"},
        "surveillance": {"status": "online", "uptime": "99.5%", "last_check": "5 min ago"},
        "metadata_analyzer": {"status": "online", "uptime": "100%", "last_check": "1 min ago"},
        "social_engineering": {"status": "online", "uptime": "99.7%", "last_check": "3 min ago"},
        "dfir": {"status": "online", "uptime": "100%", "last_check": "2 min ago"},
        "vpn_proxy_manager": {"status": "online", "uptime": "99.9%", "last_check": "Just now"}
    },
    "traffic_sources": {
        "direct": 45,
        "search": 25,
        "social": 15,
        "referral": 10,
        "other": 5
    },
    "popular_pages": [
        {"/vpn_proxy": 340},
        {"/": 250},
        {"/health": 120},
        {"/dashboard": 89}
    ],
    "hourly_traffic": [random.randint(10, 80) for _ in range(24)]
}

# Activity Log
activity_log = [
    {"id": 1, "timestamp": datetime.now().isoformat(), "user": "admin", "action": "Login", "details": "Successful login from 192.168.1.1", "type": "auth", "ip": "192.168.1.1"},
    {"id": 2, "timestamp": (datetime.now() - timedelta(minutes=5)).isoformat(), "user": "admin", "action": "VPN Connect", "details": "Connected to US East server", "type": "system", "ip": "192.168.1.1"},
    {"id": 3, "timestamp": (datetime.now() - timedelta(minutes=10)).isoformat(), "user": "admin", "action": "Proxy Detection", "details": "Analyzed IP: 8.8.8.8 - Result: Clean", "type": "security", "ip": "192.168.1.1"},
    {"id": 4, "timestamp": (datetime.now() - timedelta(minutes=15)).isoformat(), "user": "admin", "action": "Leak Test", "details": "No leaks detected", "type": "security", "ip": "192.168.1.1"},
    {"id": 5, "timestamp": (datetime.now() - timedelta(hours=1)).isoformat(), "user": "system", "action": "Auto Backup", "details": "Database backup completed", "type": "system", "ip": "localhost"},
]

# User Settings (Theme)
user_settings = {
    "theme": "dark",
    "language": "ar",
    "sidebar_collapsed": False,
    "notifications_enabled": True,
    "auto_refresh": True
}

# ═══════ Routes ═════

@bp.route('/')
def dashboard():
    return render_template_string(ANALYTICS_DASHBOARD)

@bp.route('/api/stats')
def api_stats():
    """Get analytics statistics"""
    # Update some dynamic values
    analytics_data["total_visits"] += random.randint(0, 3)
    analytics_data["active_connections"] = max(1, len(activity_log))
    analytics_data["requests_today"] += random.randint(0, 5)
    
    return jsonify({"success": True, "data": analytics_data})

@bp.route('/api/activity')
def api_activity():
    """Get activity log"""
    return jsonify({
        "success": True, 
        "count": len(activity_log),
        "data": activity_log[-50:]  # Last 50 entries
    })

@bp.route('/api/activity/add', methods=['POST'])
def api_add_activity():
    """Add new activity entry"""
    data = request.json or {}
    new_entry = {
        "id": len(activity_log) + 1,
        "timestamp": datetime.now().isoformat(),
        "user": data.get("user", "unknown"),
        "action": data.get("action", "Unknown action"),
        "details": data.get("details", ""),
        "type": data.get("type", "general"),
        "ip": data.get("ip", request.remote_addr)
    }
    activity_log.insert(0, new_entry)
    return jsonify({"success": True, "entry": new_entry})

@bp.route('/api/settings')
def api_settings():
    """Get user settings"""
    return jsonify({"success": True, "settings": user_settings})

@bp.route('/api/settings/update', methods=['POST'])
def api_update_settings():
    """Update user settings"""
    global user_settings
    data = request.json or {}
    
    if "theme" in data:
        user_settings["theme"] = data["theme"]
    if "language" in data:
        user_settings["language"] = data["language"]
    if "sidebar_collapsed" in data:
        user_settings["sidebar_collapsed"] = data["sidebar_collapsed"]
        
    return jsonify({"success": True, "settings": user_settings})

@bp.route('/api/clear-logs', methods=['POST'])
def api_clear_logs():
    """Clear activity log"""
    global activity_log
    activity_log = []
    return jsonify({"success": True, "message": "Activity log cleared"})

# ═════ HTML Template ═════

ANALYTICS_DASHBOARD = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>📊 Dashboard Analytics | Security Toolkit</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        :root{--primary:#6f42c1;--dark:#0f0f23;--card:#1a1a3e;--success:#198754;--danger:#dc3545;--warning:#ffc107}
        *{box-sizing:border-box}
        body{background:var(--dark);color:#eee;font-family:'Segoe UI',sans-serif;margin:0;padding:20px}
        .stat-card{background:linear-gradient(135deg,rgba(111,66,193,.15),rgba(102,16,242,.05));border:1px solid rgba(111,66,193,.25);border-radius:12px;padding:20px;text-align:center}
        .stat-value{font-size:2rem;font-weight:bold;color:#fff}
        .main-card{background:var(--card);border-radius:15px;border:1px solid rgba(111,66,193,.3);padding:20px;margin-bottom:20px}
        .log-entry{background:rgba(255,255,255,.03);border-right:3px solid var(--primary);padding:12px;border-radius:6px;margin-bottom:8px;font-size:.9em}
        .log-auth{border-color:var(--success)}
        .log-security{border-color:var(--warning)}
        .log-system{border-color:var(--primary)}
        .badge-status{font-size:.75em;padding:4px 10px;border-radius:12px}
        .status-online{background:rgba(25,135,84,.2);color:var(--success)}
        .status-offline{background:rgba(220,53,69,.2);color:var(--danger)}
        .theme-btn{width:40px;height:40px;border-radius:50%;border:2px solid transparent;cursor:pointer;transition:all .3s}
        .theme-btn:hover{transform:scale(1.1)}
        .theme-btn.active{border-color:#fff;box-shadow:0 0 15px currentColor}
    </style>
</head>
<body>
<div class="container-fluid">
    <!-- Header -->
    <div class="d-flex justify-content-between align-items-center mb-4">
        <h3><i class="bi bi-graph-up me-2"></i>Dashboard Analytics</h3>
        <div class="d-flex gap-2 align-items-center">
            <span class="text-muted me-2">🎨 Theme:</span>
            <button class="theme-btn active" style="background:#1a1a3e" onclick="setTheme('dark')" title="Dark"></button>
            <button class="theme-btn" style="background:#f8f9fa" onclick="setTheme('light')" title="Light"></button>
            <button class="theme-btn" style="background:linear-gradient(135deg,#667eea,#764ba2)" onclick="setTheme('purple')" title="Purple"></button>
            <button class="theme-btn" style="background:linear-gradient(135deg,#11998e,#38ef7d)" onclick="setTheme('green')" title="Green"></button>
        </div>
    </div>

    <!-- Stats Row -->
    <div class="row g-3 mb-4">
        <div class="col-md-3"><div class="stat-card"><i class="bi bi-eye fs-2 text-primary d-block mb-2"></i><div class="stat-value" id="visits">--</div><small>Total Visits</small></div></div>
        <div class="col-md-3"><div class="stat-card"><i class="bi bi-people fs-2 text-info d-block mb-2"></i><div class="stat-value" id="visitors">--</div><small>Unique Visitors</small></div></div>
        <div class="col-md-3"><div class="stat-card"><i class="bi bi-clock-history fs-2 text-warning d-block mb-2"></i><div class="stat-value" id="response">--ms</div><small>Avg Response</small></div></div>
        <div class="col-md-3"><div class="stat-card"><i class="bi bi-arrow-repeat fs-2 text-success d-block mb-2"></i><div class="stat-value">99.9%</div><small>Uptime</small></div></div>
    </div>

    <div class="row g-4">
        <div class="col-lg-8">
            <!-- Systems Status -->
            <div class="main-card">
                <h6 class="mb-3"><i class="bi bi-gear me-2"></i>Systems Status</h6>
                <div id="systems-status" class="table-responsive"></div>
            </div>

            <!-- Traffic Chart -->
            <div class="main-card">
                <h6 class="mb-3"><i class="bi bi-bar-chart me-2"></i>Traffic Overview (24h)</h6>
                <canvas id="trafficChart" height="100"></canvas>
            </div>
        </div>

        <div class="col-lg-4">
            <!-- Activity Log -->
            <div class="main-card">
                <div class="d-flex justify-content-between align-items-center mb-3">
                    <h6 class="mb-0"><i class="bi bi-journal-text me-2"></i>Activity Log</h6>
                    <button class="btn btn-sm btn-outline-danger" onclick="clearLogs()">Clear</button>
                </div>
                <div id="activity-log" style="max-height:400px;overflow-y:auto"></div>
            </div>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/js/bootstrap.bundle.min.js"></script>
<script>
// Load Data
document.addEventListener('DOMContentLoaded', function() {
    loadStats();
    loadActivity();
    setInterval(loadStats, 30000);
});

async function loadStats() {
    const r = await fetch('/analytics/api/stats');
    const d = await r.json();
    if(d.success) {
        document.getElementById('visits').textContent = d.data.total_visits;
        document.getElementById('visitors').textContent = d.data.unique_visitors;
        document.getElementById('response').textContent = d.data.avg_response_time + 'ms';
        
        // Systems Status
        let html = '<table class="table table-sm table-borderless">';
        for(let [sys, info] of Object.entries(d.data.systems_status)) {
            html += `<tr>
                <td>${sys.replace(/_/g,' ')}</td>
                <td><span class="badge badge-status ${info.status==='online'?'status-online':'status-offline'}">${info.status}</span></td>
                <td class="text-muted small">${info.uptime}</td>
            </tr>`;
        }
        html += '</table>';
        document.getElementById('systems-status').innerHTML = html;
        
        // Chart
        if(window.myChart) window.myChart.destroy();
        const ctx = document.getElementById('trafficChart').getContext('2d');
        window.myChart = new Chart(ctx, {
            type: 'line',
            data: {
                labels: Array.from({length:24},(_,i)=>`${i}:00`),
                datasets: [{
                    label: 'Requests',
                    data: d.data.hourly_traffic,
                    borderColor: '#6f42c1',
                    backgroundColor: 'rgba(111,66,193,0.1)',
                    fill: true,
                    tension: 0.4
                }]
            },
            options: {responsive:true,plugins:{legend:{display:false}},
                scales:{y:{beginAtZero:true,ticks:{color:'#888'}},x:{ticks:{color:'#888'}}}}
        });
    }
}

async function loadActivity() {
    const r = await fetch('/analytics/api/activity');
    const d = await r.json();
    const container = document.getElementById('activity-log');
    container.innerHTML = d.data.map(entry => `
        <div class="log-entry log-${entry.type}">
            <div class="d-flex justify-content-between">
                <strong>${entry.action}</strong>
                <small class="text-muted">${new Date(entry.timestamp).toLocaleTimeString()}</small>
            </div>
            <small class="text-muted">${entry.details}</small>
            <div><span class="text-info">${entry.user}</span> • ${entry.ip}</div>
        </div>`).join('');
}

function setTheme(theme) {
    fetch('/analytics/api/settings/update', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({theme})
    });
    document.querySelectorAll('.theme-btn').forEach(b=>b.classList.remove('active'));
    event.target.classList.add('active');
    // Apply theme logic here
    if(theme==='light') document.body.style.background='#f8f9fa';
    else if(theme==='dark') document.body.style.background='#0f0f23';
}

async function clearLogs() {
    if(!confirm('Clear all logs?')) return;
    await fetch('/analytics/api/clear-logs',{method:'POST'});
    loadActivity();
}
</script>
</body></html>'''

def init_app(app):
    app.register_blueprint(bp, url_prefix='/analytics')
