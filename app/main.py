"""
ADVANCED SECURITY TOOLKIT PRO v4.0
Final Version - With Beautiful UI
"""

import os
from app import create_app

app = create_app()

@app.route('/')
def home():
    return '''
<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🛡️ Security Toolkit PRO v4.0</title>
    
    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Tajawal:wght@400;700&family=Cairo:wght@400;600&display=swap" rel="stylesheet">
    
    <!-- Bootstrap 5 -->
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://cdn.jsdelivr.net/npm/bootstrap-icons@1.11.0/font/bootstrap-icons.min.css" rel="stylesheet">
    
    <style>
        :root {
            --bg-primary: #0f0f23;
            --bg-card: #1a1a3e;
            --primary: #6f42c1;
            --primary-dark: #5a329a;
            --success: #198754;
            --danger: #dc3545;
            --warning: #ffc107;
            --text-primary: #e0e0e0;
            --text-muted: #888888;
            --border-color: rgba(111,66,193,0.2);
            --shadow: 0 10px 30px rgba(0,0,0,0.3);
            --radius: 16px;
            --radius-sm: 8px;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            background-color: var(--bg-primary);
            color: var(--text-primary);
            font-family: 'Cairo', 'Tajawal', sans-serif;
            min-height: 100vh;
            line-height: 1.6;
            overflow-x: hidden;
        }
        
        /* ===== NAVBAR ===== */
        .navbar-custom {
            background: linear-gradient(135deg, #16213e 0%, #0f0f23 100%);
            border-bottom: 2px solid var(--primary);
            padding: 15px 0;
            box-shadow: var(--shadow);
        }
        
        .navbar-brand {
            font-weight: 700;
            font-size: 1.3rem;
            color: var(--primary) !important;
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .navbar-brand i {
            font-size: 1.5rem;
        }
        
        /* ===== HERO SECTION ===== */
        .hero-section {
            padding: 80px 20px 60px;
            text-align: center;
        }
        
        .hero-title {
            font-size: 3rem;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            margin-bottom: 20px;
        }
        
        .hero-badge {
            display: inline-flex;
            align-items: center;
            gap: 12px;
            background: rgba(25, 135, 84, 0.15);
            border: 1px solid rgba(25, 135, 84, 0.3);
            padding: 10px 24px;
            border-radius: 50px;
            font-size: 1.1em;
            color: var(--success);
        }
        
        .hero-subtitle {
            font-size: 1.2rem;
            color: var(--text-muted);
            max-width: 600px;
            margin: 0 auto;
        }
        
        /* ===== SYSTEMS GRID ===== */
        .systems-container {
            padding: 40px 20px 60px;
            max-width: 1400px;
            margin: 0 auto;
        }
        
        .section-title {
            text-align: center;
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 40px;
            position: relative;
            padding-bottom: 15px;
        }
        
        .section-title::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;
            transform: translateX(-50%);
            width: 100px;
            height: 3px;
            background: var(--primary);
            border-radius: 3px;
        }
        
        .systems-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
            gap: 25px;
        }
        
        /* ===== SYSTEM CARD ===== */
        .system-card {
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius);
            padding: 30px;
            transition: all 0.3s ease;
            text-decoration: none;
            color: var(--text-primary) !important;
            display: block;
            position: relative;
            overflow: hidden;
        }
        
        .system-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.4);
            border-color: var(--primary);
        }
        
        .system-icon {
            font-size: 3rem;
            margin-bottom: 20px;
            display: block;
        }
        
        .system-name {
            font-size: 1.4rem;
            font-weight: 700;
            margin-bottom: 10px;
            color: #fff;
        }
        
        .system-desc {
            color: var(--text-muted);
            font-size: 0.95rem;
            line-height: 1.6;
            margin-bottom: 20px;
        }
        
        .system-status {
            display: inline-block;
            padding: 6px 16px;
            border-radius: 20px;
            font-size: 0.85em;
            font-weight: 600;
        }
        
        .status-online { background: rgba(25, 135, 84, 0.2); color: var(--success); }
        .status-beta { background: rgba(255, 193, 7, 0.2); color: var(--warning); }
        .status-offline { background: rgba(220, 53, 69, 0.2); color: var(--danger); }
        
        .btn-system {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 14px 28px;
            background: linear-gradient(135deg, var(--primary), var(--primary-dark));
            color: white !important;
            border: none;
            border-radius: 50px;
            text-decoration: none;
            font-weight: 600;
            font-size: 1rem;
            transition: all 0.3s ease;
        }
        
        .btn-system:hover {
            transform: scale(1.05);
            box-shadow: 0 10px 25px rgba(111, 66, 193, 0.4);
        }
        
        /* ===== FOOTER ===== */
        .footer {
            background: linear-gradient(180deg, #16213e 0%, #0f0f23 100%);
            border-top: 1px solid var(--border-color);
            padding: 40px 20px;
            text-align: center;
            color: var(--text-muted);
            margin-top: 60px;
        }
        
        /* ===== RESPONSIVE ===== */
        @media (max-width: 768px) {
            .hero-title { font-size: 2rem; }
            .systems-grid { grid-template-columns: 1fr; gap: 15px; }
            .systems-container { padding: 30px 15px; }
        }
    </style>
</head>
<body>

    <!-- Navbar -->
    <nav class="navbar navbar-expand-lg navbar-dark navbar-custom">
        <div class="container-fluid px-4">
            <a class="navbar-brand" href="/">
                <i class="bi bi-shield-lock-fill me-2"></i>
                Security Toolkit PRO
            </a>
            <span class="badge bg-success ms-3">v4.0</span>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="hero-section">
        <div class="hero-title">🛡️ Security Toolkit PRO</div>
        <div class="hero-badge">
            <i class="bi bi-check-circle-fill me-2"></i>
            System Online • 13 Active Systems
        </div>
        <p class="hero-subtitle">
            نظام أمن متكامل مع 13 نظام أمني متخصص
        </p>
    </section>

    <!-- Systems Grid -->
    <section class="systems-container">
        <h2 class="section-title">🛡️ All Security Systems</h2>
        
        <div class="systems-grid">
            
            <!-- System 1: Network Monitor -->
            <a href="/network" class="system-card">
                <span class="system-icon">📡</span>
                <div class="system-name">Network Monitor</div>
                <div class="system-desc">مراقبة الشبكة في الوقت الحقي<br>كشف التهديدات ومنع الهجمات</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 2: Link Tracker -->
            <a href="/tracker" class="system-card">
                <span class="system-icon">🔗</span>
                <div class="system-name">Link Tracker</div>
                <div class="system-desc">إنشاء روابط قصيرة وتتبع حركة النقرارات<br>تحليل جغرافي للمستخدمين</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 3: Parental Control -->
            <a href="/parental" class="system-card">
                <span class="system-icon">👨‍👩‍👧</span>
                <div class="system-name">Parental Control</div>
                <div class="system-desc">فلترة المواقع الضارة وإدارة الوقت<br>مراقبة نشاط الأطفال</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 4: Surveillance -->
            <a href="/surveillance" class="system-card">
                <span class="system-icon">🕵️</span>
                <div class="system-name">Surveillance</div>
                <div class="system-desc">نظام مراقبة متقدم IDS/IPS<br>تحليل سلوك ونمذجاة سلوكية</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 5: Metadata Analyzer -->
            <a href="/metadata" class="system-card">
                <span class="system-icon">📱</span>
                <div class="system-name">Metadata Analyzer</div>
                <div class="system-desc">استخراج بيانات EXIF/GPS من الصور والملفات<br>كشف الصور المزيفة</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 6: Social Engineering -->
            <a href="/social" class="system-card">
                <span class="system-icon">🎭</span>
                <div class="system-name">Social Engineering</div>
                <div class="system-desc">محاكاة صفحات Phishing آلية<br>اختبار وعيوب الأماني</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 7: DFIR Forensics -->
            <a href="/dfir" class="system-card">
                <span class="system-icon">🔬</span>
                <div class="system-name">DFIR Forensics</div>
                <div class="system-desc">أدوات الطب الشرعي الرقمي<br>تحليل الزمن وجمعالجة الأدلة</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 8: VPN Manager ⭐ -->
            <a href="/vpn_proxy" class="system-card" style="border-color: var(--primary);">
                <span class="system-icon">🌐</span>
                <div class="system-name">VPN Proxy Manager ⭐</div>
                <div class="system-desc">إدارة VPN و Proxy Chains<br>كشف تسريب IP وكشف البروكسي</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 9+11+16: Analytics -->
            <a href="/analytics" class="system-card">
                <span class="system-icon">📊</span>
                <div class="system-name">Analytics & Theme</div>
                <div class="system-desc">إحصائيات واستخدام النظام<br>تبديل الألوان (Dark/Light)</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 10+12: Users -->
            <a href="/users" class="system-card">
                <span class="system-icon">👥</span>
                <div class="system-name">Users & Notifications</div>
                <div class="system-desc">إدارة المستخدمين والصلاحيات<br>إشعارات فورية</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

            <!-- System 13+14+15: Reports -->
            <a href="/reports" class="system-card">
                <span class="system-icon">📈</span>
                <div class="system-name">Reports & Backup</div>
                <div class="system-desc">تقاريرات PDF/Excel<br>نسخ احتياطي تلقائي</div>
                <span class="system-status status-online">● شغال</span>
                <br><div class="btn-system"><i class="bi bi-arrow-left me-1"></i>فتح النظام</div>
            </a>

        </div>
    </section>

    <!-- Footer -->
    <footer class="footer">
        <p>&copy; 2024 Security Toolkit PRO | All Rights Reserved</p>
        <p style="margin-top:10px;font-size:.9em;">
            Made with ❤️ | Deployed on Render Cloud ☁️
        </p>
    </footer>

</body>
</html>
'''


@app.route('/health')
def health():
    return {"status": "healthy", "version": "4.0", "systems": 13}, 200


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
