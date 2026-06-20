"""
ADVANCED SECURITY TOOLKIT PRO v4.0
Main Entry Point - Render Compatible Version
"""

from app import create_app
import os

# Create Flask app (NO SocketIO!)
app = create_app()


@app.route('/')
def index():
    '''Main Landing Page'''
    return '''
<!DOCTYPE html>
<html>
<head>
    <title>Security Toolkit PRO v4.0</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1a1a2e, #16213e);
            color: #ffffff;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            margin: 0;
            padding: 20px;
        }
        .container {
            text-align: center;
            padding: 50px;
            background: rgba(255, 255, 255, 0.05);
            border-radius: 25px;
            box-shadow: 0 20px 60px rgba(0, 0, 0, 0.5);
            max-width: 700px;
        }
        h1 {
            font-size: 3em;
            color: #6f42c1;
            margin-bottom: 15px;
        }
        .status {
            color: #00ff88;
            font-size: 1.3em;
            margin: 20px 0;
        }
        .systems {
            color: #aaaaaa;
            line-height: 2;
            margin: 30px 0;
        }
        a {
            display: inline-block;
            margin-top: 30px;
            padding: 15px 40px;
            background: linear-gradient(135deg, #6f42c1, #6610f2);
            color: white;
            text-decoration: none;
            border-radius: 50px;
            font-size: 1.2em;
            transition: transform 0.3s, box-shadow 0.3s;
        }
        a:hover {
            transform: translateY(-3px);
            box-shadow: 0 10px 30px rgba(111, 66, 193, 0.5);
        }
        .badge {
            background: rgba(0, 255, 136, 0.2);
            color: #00ff88;
            padding: 8px 20px;
            border-radius: 20px;
            font-size: 0.9em;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🛡️ Security Toolkit PRO</h1>
        <div class="badge">✅ System Online | Version 4.0</div>
        
        <div class="systems">
            <strong>8 Advanced Security Systems Running:</strong><br><br>
            📡 Network Monitor &nbsp;|&nbsp; 🔗 Link Tracker &nbsp;|&nbsp; 👨‍👩‍👧 Parental Control<br><br>
            🕵️ Surveillance &nbsp;|&nbsp; 📱 Metadata Analyzer &nbsp;|&nbsp; 🎭 Social Engineering<br><br>
            🔬 DFIR Forensics &nbsp;|&nbsp; 🌐 <strong>VPN Proxy Manager ⭐</strong>
        </div>
        
        <a href="/vpn_proxy">→ Go to VPN Proxy Manager Dashboard →</a>
    </div>
</body>
</html>
'''


@app.route('/health')
def health_check():
    '''Health check endpoint for Render'''
    return {
        'status': 'healthy',
        'version': '4.0',
        'systems': 8,
        'message': 'All systems operational'
    }, 200


# Run the app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
