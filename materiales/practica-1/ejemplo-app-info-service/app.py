"""
App Info Service - Aplicación Flask de ejemplo para S12
Demuestra uso de variables de entorno, secretos y despliegue en Cloud Run
"""

from flask import Flask, jsonify
import os
from datetime import datetime

app = Flask(__name__)

# Contador simple en memoria (muestra escalado en Cloud Run) patata
request_count = 0

@app.route('/')
def index():
    """Endpoint principal con información del servicio"""
    return {
        'service': 'App Info Service',
        'version': '1.0.0',
        'description': 'Servicio de ejemplo para demostrar CI/CD y Cloud Run',
        'endpoints': [
            '/health',
            '/info',
            '/config',
            '/secret',
            '/stats'
        ]
    }

@app.route('/health')
def health():
    """Health check endpoint requerido por Cloud Run"""
    return {
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat()
    }

@app.route('/info')
def info():
    """Información del contenedor y entorno"""
    return {
        'hostname': os.environ.get('HOSTNAME', 'unknown'),
        'description': 'Información de la APP'
        'environment': os.environ.get('ENVIRONMENT', 'not-set'),
        'app_name': os.environ.get('APP_NAME', 'not-set'),
        'port': os.environ.get('PORT', 'not-set')
    }

@app.route('/config')
def config():
    """Muestra configuración sin exponer valores sensibles de secretos"""
    return {
        'app_name': os.environ.get('APP_NAME'),
        'environment': os.environ.get('ENVIRONMENT'),
        'has_secret_message': bool(os.environ.get('SECRET_MESSAGE')),
        'has_api_key': bool(os.environ.get('API_KEY')),
        'note': 'Los secretos no se exponen por seguridad'
    }

@app.route('/secret')
def secret():
    """Endpoint que requiere un secreto desde Secret Manager"""
    secret_msg = os.environ.get('SECRET_MESSAGE')
    if not secret_msg:
        return {
            'error': 'Secret not configured',
            'message': 'La variable SECRET_MESSAGE no está configurada'
        }, 500
    
    return {
        'secret_message': secret_msg,
        'note': 'Este mensaje viene de Secret Manager'
    }

@app.route('/stats')
def stats():
    """
    Estadísticas simples en memoria.
    En Cloud Run, cada instancia tiene su propio contador,
    demostrando el escalado horizontal.
    """
    global request_count
    request_count += 1
    return {
        'requests_handled': request_count,
        'hostname': os.environ.get('HOSTNAME', 'unknown'),
        'note': 'Este contador se resetea en cada instancia de Cloud Run',
        'environment': os.environ.get('ENVIRONMENT', 'not-set')
    }

if __name__ == '__main__':
    # Cloud Run establece PORT automáticamente
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)

