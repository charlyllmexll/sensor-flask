from flask import Flask, jsonify, render_template_string
from datetime import datetime
import threading
import requests
import logging

app = Flask(__name__)

# =========================
# CONFIGURACIÓN
# =========================

WHATSAPP_PHONE = "5213338517153"
API_KEY = "3939038"

# Anti-spam
ULTIMO_EVENTO = None
TIEMPO_MINIMO = 10

# Historial
eventos = []

# Logs
logging.basicConfig(level=logging.INFO)

# =========================
# FUNCIÓN WHATSAPP
# =========================

def enviar_whatsapp(mensaje):
    try:
        url = "https://api.callmebot.com/whatsapp.php"

        params = {
            "phone": WHATSAPP_PHONE,
            "text": mensaje,
            "apikey": API_KEY
        }

        response = requests.get(url, params=params, timeout=10)

        logging.info(f"WhatsApp enviado: {response.status_code}")

    except Exception as e:
        logging.error(f"Error WhatsApp: {e}")

# =========================
# API MOVIMIENTO
# =========================

@app.route('/movimiento', methods=['GET'])
def movimiento():

    global ULTIMO_EVENTO

    ahora = datetime.now()

    # Anti-spam
    if ULTIMO_EVENTO:
        diferencia = (ahora - ULTIMO_EVENTO).seconds

        if diferencia < TIEMPO_MINIMO:
            return "IGNORADO", 200

    ULTIMO_EVENTO = ahora

    # Evento
    evento = {
        "fecha": ahora.strftime("%d/%m/%Y"),
        "hora": ahora.strftime("%H:%M:%S"),
        "mensaje": "Movimiento detectado"
    }

    eventos.append(evento)

    logging.info(f"Evento recibido: {evento}")

    # Mensaje WhatsApp
    mensaje = (
        "🚨 Movimiento detectado\n"
        f"📅 Fecha: {evento['fecha']}\n"
        f"⏰ Hora: {evento['hora']}"
    )

    # 🔥 ENVÍO ASÍNCRONO
    hilo = threading.Thread(
        target=enviar_whatsapp,
        args=(mensaje,)
    )

    hilo.start()

    return jsonify({
        "status": "ok",
        "evento": evento
    })

# =========================
# API EVENTOS
# =========================

@app.route('/eventos', methods=['GET'])
def ver_eventos():
    return jsonify(eventos)

# =========================
# DASHBOARD WEB
# =========================

@app.route('/')
def dashboard():

    html = """
    <html>
    <head>
        <title>Monitor IoT</title>

        <meta http-equiv="refresh" content="3">

        <style>
            body{
                font-family: Arial;
                background:#121212;
                color:white;
                padding:20px;
            }

            .card{
                background:#1f1f1f;
                padding:15px;
                margin-bottom:10px;
                border-radius:10px;
            }

            h1{
                color:#00ff99;
            }
        </style>
    </head>

    <body>

        <h1>🚨 Monitor de Movimiento</h1>

        {% for evento in eventos %}

        <div class="card">
            <h3>{{evento.mensaje}}</h3>

            <p>📅 {{evento.fecha}}</p>
            <p>⏰ {{evento.hora}}</p>
        </div>

        {% endfor %}

    </body>
    </html>
    """

    return render_template_string(
        html,
        eventos=reversed(eventos[-20:])
    )

# =========================
# LIMPIAR EVENTOS
# =========================

@app.route('/limpiar')
def limpiar():

    eventos.clear()

    return "Eventos eliminados"

# =========================
# MAIN
# =========================

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
