"""
Evaluación N°2 - DRY7122
Parte 3: Aplicación web desplegada con Docker + Jenkins (CI/CD)
"""
from flask import Flask
from datetime import datetime

app = Flask(__name__)

@app.route('/')
def home():
    return f"""
    <html>
      <head><title>Eva2 DRY7122</title></head>
      <body style="font-family:Arial;text-align:center;padding:50px;background:#1e1e2e;color:#cdd6f4">
        <h1>🚀 Evaluación N°2 - DRY7122</h1>
        <h2>Parte 3: Docker + Jenkins CI/CD</h2>
        <p>Aplicación desplegada exitosamente con Jenkins</p>
        <p>Puerto: 9999</p>
        <p>Hora servidor: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</p>
        <hr>
        <p>Autor: [Manuel Arrué y Jairo Soto]</p>
      </body>
    </html>
    """

@app.route('/health')
def health():
    return {"status": "ok", "service": "eva2-app"}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9999)
