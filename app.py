from flask import Flask, jsonify
from datetime import datetime
import requests
import os

app = Flask(__name__)

eventos = []

# 🔴 CONFIGURA AQUÍ
WHATSAPP_PHONE = "5213338517153"  # tu número con lada (México = 521)
API_KEY = "3939038"

@app.route('/')
def home():
    return "Servidor activo"

@app.route('/movimiento', methods=['GET'])
def movimiento():
    evento = f"Movimiento detectado - {datetime.now()}"
    print(evento)
    eventos.append(evento)

    try:
        url = "https://api.callmebot.com/whatsapp.php"
        params = {
            "phone": WHATSAPP_PHONE,
            "text": "🚨 Movimiento detectado",
            "apikey": API_KEY
        }
        requests.get(url, params=params)
    except Exception as e:
        print("Error WhatsApp:", e)

    return "OK", 200

@app.route('/eventos', methods=['GET'])
def ver_eventos():
    return jsonify(eventos)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)