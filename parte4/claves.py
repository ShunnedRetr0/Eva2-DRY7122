"""
========================================================
Evaluación N°2 - DRY7122
Parte 4: Control de Credenciales con Flask + SQLite

Este servicio permite:
  - Registrar nuevos usuarios con contraseña hasheada
  - Validar credenciales contra la base de datos
  - Listar usuarios registrados (sin exponer contraseñas)

Las contraseñas se almacenan con hash SHA-256 + salt
mediante werkzeug.security (NUNCA en texto plano).

Autores: [Manuel Arrué y Jairo Soto]
Fecha: [21/05/2026]
========================================================
"""

from flask import Flask, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from datetime import datetime

# ============================================
# CONFIGURACIÓN
# ============================================
app = Flask(__name__)
DB_NAME = "credenciales.db"


# ============================================
# INICIALIZACIÓN DE LA BASE DE DATOS
# ============================================
def init_db():
    """Crea la tabla de usuarios si no existe."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            fecha_registro TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()
    print(f"✅ Base de datos '{DB_NAME}' lista.")


# ============================================
# ENDPOINTS
# ============================================
@app.route("/", methods=["GET"])
def home():
    """Endpoint informativo."""
    return jsonify({
        "servicio": "Control de Credenciales DRY7122",
        "endpoints": {
            "POST /registrar": "Registra un nuevo usuario",
            "POST /validar":   "Valida credenciales",
            "GET  /usuarios":  "Lista usuarios registrados"
        }
    })


@app.route("/registrar", methods=["POST"])
def registrar():
    """
    Registra un nuevo usuario.
    Body JSON: {"usuario": "nombre", "password": "clave"}
    """
    datos = request.get_json()
    
    if not datos or "usuario" not in datos or "password" not in datos:
        return jsonify({"error": "Faltan campos 'usuario' o 'password'"}), 400
    
    usuario = datos["usuario"].strip()
    password = datos["password"]
    
    if not usuario or not password:
        return jsonify({"error": "Usuario y contraseña no pueden estar vacíos"}), 400
    
    # Hashear la contraseña antes de almacenarla
    password_hash = generate_password_hash(password, method="pbkdf2:sha256")
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO usuarios (usuario, password_hash, fecha_registro) VALUES (?, ?, ?)",
            (usuario, password_hash, fecha)
        )
        conn.commit()
        conn.close()
        
        return jsonify({
            "mensaje": "✅ Usuario registrado correctamente",
            "usuario": usuario,
            "fecha_registro": fecha
        }), 201
    
    except sqlite3.IntegrityError:
        return jsonify({"error": f"El usuario '{usuario}' ya existe"}), 409
    except Exception as e:
        return jsonify({"error": f"Error al registrar: {str(e)}"}), 500


@app.route("/validar", methods=["POST"])
def validar():
    """
    Valida las credenciales de un usuario.
    Body JSON: {"usuario": "nombre", "password": "clave"}
    """
    datos = request.get_json()
    
    if not datos or "usuario" not in datos or "password" not in datos:
        return jsonify({"error": "Faltan campos 'usuario' o 'password'"}), 400
    
    usuario = datos["usuario"].strip()
    password = datos["password"]
    
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT password_hash FROM usuarios WHERE usuario = ?",
        (usuario,)
    )
    resultado = cursor.fetchone()
    conn.close()
    
    if resultado is None:
        return jsonify({
            "autenticado": False,
            "mensaje": "❌ Usuario no encontrado"
        }), 404
    
    password_hash = resultado[0]
    
    if check_password_hash(password_hash, password):
        return jsonify({
            "autenticado": True,
            "mensaje": "✅ Credenciales válidas",
            "usuario": usuario
        }), 200
    else:
        return jsonify({
            "autenticado": False,
            "mensaje": "❌ Contraseña incorrecta"
        }), 401


@app.route("/usuarios", methods=["GET"])
def listar_usuarios():
    """Lista todos los usuarios registrados (sin exponer contraseñas)."""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, usuario, fecha_registro FROM usuarios")
    filas = cursor.fetchall()
    conn.close()
    
    usuarios = [
        {"id": fila[0], "usuario": fila[1], "fecha_registro": fila[2]}
        for fila in filas
    ]
    
    return jsonify({
        "total": len(usuarios),
        "usuarios": usuarios
    })


# ============================================
# MAIN
# ============================================
if __name__ == "__main__":
    print("=" * 60)
    print("  SERVICIO DE CONTROL DE CREDENCIALES")
    print("  Evaluación N°2 DRY7122")
    print(f"  Iniciado: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print("=" * 60)
    
    init_db()
    
    print("\n🚀 Servidor corriendo en http://localhost:5000")
    print("   Endpoints disponibles:")
    print("   - POST /registrar  → Registrar usuario")
    print("   - POST /validar    → Validar credenciales")
    print("   - GET  /usuarios   → Listar usuarios")
    print("\n   Presiona CTRL+C para detener\n")
    
    app.run(host="0.0.0.0", port=5000, debug=False)