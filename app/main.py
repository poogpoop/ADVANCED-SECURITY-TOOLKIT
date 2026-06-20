import os
from app import create_app
app = create_app()

@app.route('/')
def home():
    return '<h1 style="color:#fff;text-align:center;padding:50px;background:#0f0f23;min-height:100vh;font-family:sans-serif">Security Toolkit PRO v4.0<br><a href="/core" style="color:#6f42c1">All Systems</a></h1>'

@app.route('/health')
def health():
    return {"status": "ok"}, 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
