"""
System #10: User Management
System #12: Notifications System
"""

from flask import Blueprint, jsonify, request, render_template_string
from datetime import datetime
import json
import hashlib

bp = Blueprint('users', __name__)

# ═══════ Users Database ═════

users_db = [
    {
        "id": 1,
        "username": "admin",
        "email": "admin@toolkit.com",
        "role": "super_admin",
        "status": "active",
        "created_at": "2024-01-01T00:00:00",
        "last_login": datetime.now().isoformat(),
        "permissions": ["all"],
        "avatar": "👨‍💻"
    }
]

roles = {
    "super_admin": {"level": 4, "permissions": ["all"], "description": "Full access"},
    "admin": {"level": 3, "permissions": ["manage_users", "view_logs", "manage_systems"], "description": "Administrator"},
    "editor": {"level": 2, "permissions": ["edit_content", "view_reports"], "description": "Content Editor"},
    "viewer": {"level": 1, "permissions": ["view_only"], "description": "Read-only access"}
}

# Notifications
notifications = [
    {"id": 1, "type": "success", "title": "System Online", "message": "All systems are operational", "time": "2 min ago", "read": False},
    {"id": 2, "type": "warning", "title": "High CPU Usage", "message": "CPU usage at 85%", "time": "15 min ago", "read": False},
    {"id": 3, "type": "info", "title": "Backup Complete", "message": "Daily backup completed successfully", "time": "1 hour ago", "read": True},
    {"id": 4, "type": "danger", "title": "Failed Login Attempt", "message": "Invalid login from 203.0.113.45", "time": "3 hours ago", "read": True},
]

# ═══════ Routes ═════

@bp.route('/')
def users_dashboard():
    return render_template_string(USERS_DASHBOARD)

@bp.route('/api/users')
def api_users():
    return jsonify({"success": True, "count": len(users_db), "users": users_db})

@bp.route('/api/users/<int:user_id>')
def api_get_user(user_id):
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return jsonify({"success": False, "error": "User not found"}), 404
    return jsonify({"success": True, "user": user})

@bp.route('/api/users/add', methods=['POST'])
def api_add_user():
    data = request.json or {}
    new_user = {
        "id": len(users_db) + 1,
        "username": data.get("username", f"user_{len(users_db)+1}"),
        "email": data.get("email", ""),
        "role": data.get("role", "viewer"),
        "status": "active",
        "created_at": datetime.now().isoformat(),
        "last_login": None,
        "permissions": roles.get(data.get("role", "viewer"), {}).get("permissions", []),
        "avatar": "👤"
    }
    users_db.append(new_user)
    return jsonify({"success": True, "user": new_user})

@bp.route('/api/users/<int:user_id>/update', methods=['POST'])
def api_update_user(user_id):
    data = request.json or {}
    user = next((u for u in users_db if u["id"] == user_id), None)
    if not user:
        return jsonify({"success": False}), 404
    
    if "role" in data:
        user["role"] = data["role"]
        user["permissions"] = roles.get(data["role"], {}).get("permissions", [])
    if "status" in data:
        user["status"] = data["status"]
    if "email" in data:
        user["email"] = data["email"]
        
    return jsonify({"success": True, "user": user})

@bp.route('/api/users/<int:user_id>/delete', methods=['DELETE'])
def api_delete_user(user_id):
    global users_db
    users_db = [u for u in users_db if u["id"] != user_id]
    return jsonify({"success": True})

@bp.route('/api/roles')
def api_roles():
    return jsonify({"success": True, "roles": roles})

@bp.route('/api/notifications')
def api_notifications():
    unread = sum(1 for n in notifications if not n["read"])
    return jsonify({"success": True, "count": len(notifications), "unread": unread, "data": notifications})

@bp.route('/api/notifications/<int:notif_id>/read', methods=['POST'])
def api_mark_read(notif_id):
    for n in notifications:
        if n["id"] == notif_id:
            n["read"] = True
            break
    return jsonify({"success": True})

@bp.route('/api/notifications/read-all', methods=['POST'])
def api_read_all():
    for n in notifications:
        n["read"] = True
    return jsonify({"success": True})

@bp.route('/api/notifications/add', methods=['POST'])
def api_add_notification():
    data = request.json or {}
    new_notif = {
        "id": len(notifications) + 1,
        "type": data.get("type", "info"),
        "title": data.get("title", "Notification"),
        "message": data.get("message", ""),
        "time": "Just now",
        "read": False
    }
    notifications.insert(0, new_notif)
    return jsonify({"success": True, "notification": new_notif})

# ═════ HTML Template ═════

USERS_DASHBOARD = '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>👥 Users & Notifications | Security Toolkit</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.10.0/font/bootstrap-icons.css" rel="stylesheet">
    <style>
        :root{--primary:#6f42c1;--dark:#0f0f23;--card:#1a1a3e}
        *{box-sizing:border-box}
        body{background:var(--dark);color:#eee;font-family:'Segoe UI',sans-serif;margin:0;padding:20px}
        .main-card{background:var(--card);border-radius:15px;border:1px solid rgba(111,66,193,.3);padding:20px;margin-bottom:20px}
        .user-row{background:rgba(255,255,255,.03);border-radius:10px;padding:15px;margin-bottom:10px;display:flex;align-items:center;justify-content:space-between}
        .avatar{font-size:2rem}
        .notif-item{background:rgba(255,255,255,.03);border-radius:10px;padding:15px;margin-bottom:10px;border-right:4px solid var(--primary)}
        .notif-item.unread{border-color:#ffc107;background:rgba(255,193,7,.05)}
        .notif-success{border-color:#198754}.notif-warning{border-color:#ffc107}.notif-danger{border-color:#dc3545}
        .role-badge{font-size:.75em;padding:4px 12px;border-radius:12px}
        .role-super_admin{background:rgba(220,53,69,.2);color:#ff6b6b}
        .role-admin{background:rgba(111,66,193,.2);color:#a78bfa}
        .role-editor{background:rgba(25,135,84,.2);color:#6ee7b7}
        .role-viewer{background:rgba(108,117,125,.2);color:#adb5bd}
        .bell-icon{position:relative}
        .badge-count{position:absolute;top:-5px;right:-5px;background:#dc3545;color:#fff;border-radius:50%;min-width:18px;height:18px;font-size:.7em;display:flex;align-items:center;justify-content:center}
    </style>
</head>
<body>
<div class="container-fluid">
    <h3 class="mb-4"><i class="bi bi-people me-2"></i>User Management & Notifications</h3>
    
    <div class="row g-4">
