from flask import Flask, jsonify
from datetime import datetime
import sqlite3

app = Flask(__name__)

# =========================
# CONFIGURAR BASE DATOS
# =========================

DATABASE = 'eventos.db'


# =========================
# CREAR TABLA
# =========================

def inicializar_db():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS eventos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            fecha TEXT,
            hora TEXT,
            mensaje TEXT
        )
    ''')

    conn.commit()
    conn.close()


# =========================
# INSERTAR EVENTO
# =========================

@app.route('/movimiento', methods=['GET'])
def movimiento():

    ahora = datetime.now()

    fecha = ahora.strftime("%d/%m/%Y")
    hora = ahora.strftime("%H:%M:%S")

    mensaje = "Movimiento detectado"

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO eventos (
            fecha,
            hora,
            mensaje
        )
        VALUES (?, ?, ?)
    ''', (fecha, hora, mensaje))

    conn.commit()

    conn.close()

    print(f"[EVENTO] {fecha} {hora}")

    return jsonify({
        "status": "ok",
        "mensaje": mensaje,
        "fecha": fecha,
        "hora": hora
    })


# =========================
# OBTENER HISTORIAL
# =========================

@app.route('/eventos', methods=['GET'])
def eventos():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            id,
            fecha,
            hora,
            mensaje
        FROM eventos
        ORDER BY id DESC
    ''')

    rows = cursor.fetchall()

    conn.close()

    eventos_lista = []

    for row in rows:

        evento = {
            "id": row[0],
            "fecha": row[1],
            "hora": row[2],
            "mensaje": row[3]
        }

        eventos_lista.append(evento)

    return jsonify(eventos_lista)


# =========================
# ÚLTIMO EVENTO
# =========================

@app.route('/ultimo_evento', methods=['GET'])
def ultimo_evento():

    conn = sqlite3.connect(DATABASE)

    cursor = conn.cursor()

    cursor.execute('''
        SELECT
            id,
            fecha,
            hora,
            mensaje
        FROM eventos
        ORDER BY id DESC
        LIMIT 1
    ''')

    row = cursor.fetchone()

    conn.close()

    if row:

        evento = {
            "id": row[0],
            "fecha": row[1],
            "hora": row[2],
            "mensaje": row[3]
        }

        return jsonify(evento)

    else:

        return jsonify({
            "id": 0,
            "fecha": "--",
            "hora": "--",
            "mensaje": "Sin eventos"
        })


# =========================
# HEALTH CHECK
# =========================

@app.route('/health', methods=['GET'])
def health():

    return jsonify({
        "status": "online"
    })


# =========================
# INICIAR APP
# =========================

inicializar_db()

app.run(
    host='0.0.0.0',
    port=5000,
    debug=True
)