<<<<<<< HEAD
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

=======
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
from datetime import datetime
from flask import Flask, render_template, request, redirect, session, jsonify
import base64
import cv2
import numpy as np
from deepface import DeepFace
import mysql.connector
<<<<<<< HEAD
=======
import os
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c

# -----------------------------
# APP FLASK
# -----------------------------
app = Flask(__name__)
app.secret_key = "emocionesIA"

# -----------------------------
# CONEXIÓN MYSQL
# -----------------------------
def conectar():
    return mysql.connector.connect(
        host=os.getenv("MYSQLHOST", "localhost"),
        user=os.getenv("MYSQLUSER", "root"),
<<<<<<< HEAD
        password=os.getenv("MYSQLPASSWORD", "123"),        database=os.getenv("MYSQLDATABASE", "emotiscan"),
=======
        password=os.getenv("MYSQLPASSWORD", "123"),
        database=os.getenv("MYSQLDATABASE", "emotiscan"),
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
        port=int(os.getenv("MYSQLPORT", 3306))
    )

# -----------------------------
<<<<<<< HEAD
# CREAR TABLAS (Mejorado para cerrar conexión siempre)
# -----------------------------
def crear_bd():
    try:
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios(
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(100) UNIQUE,
            password VARCHAR(100)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS emociones(
            id INT AUTO_INCREMENT PRIMARY KEY,
            usuario VARCHAR(100),
            emocion VARCHAR(50),
            fecha_registro DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        conn.commit()
    except Exception as e:
        print(f"Error creando BD: {e}")
    finally:
        if 'conn' in locals() and conn.is_connected():
            conn.close()

crear_bd()

# Detector de rostro rápido para el pre-procesamiento
face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

=======
# CREAR TABLAS
# -----------------------------
def crear_bd():
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios(
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario VARCHAR(100) UNIQUE,
        password VARCHAR(100)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS emociones(
        id INT AUTO_INCREMENT PRIMARY KEY,
        usuario VARCHAR(100),
        emocion VARCHAR(50)
    )
    """)

    conn.commit()
    conn.close()

crear_bd()

# -----------------------------
# DETECTOR DE ROSTRO
# -----------------------------
face_detector = cv2.CascadeClassifier(
    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
)

# -----------------------------
# CONSEJOS IA
# -----------------------------
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
def consejo_emocion(emocion):
    consejos = {
        "happy": "Estás feliz 😊 aprovecha para avanzar en tus metas.",
        "sad": "Estás triste 😢 habla con alguien o descansa un poco.",
        "angry": "Respira profundo 😡 calma tu mente antes de actuar.",
<<<<<<< HEAD
        "neutral": "Estás estable 😐 buen momento para concentrarte."
=======
        "neutral": "Estás estable 😐 buen momento para concentrarte.",
        "fear": "Tranquilo 😨 todo problema tiene solución.",
        "surprise": "Algo te sorprendió 😲 analiza con calma la situación."
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
    }
    return consejos.get(emocion, "Cuida tu bienestar emocional.")

# -----------------------------
<<<<<<< HEAD
# RUTAS DE LOGIN Y REGISTRO
=======
# LOGIN
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
# -----------------------------
@app.route("/")
def login():
    return render_template("login.html")

<<<<<<< HEAD
=======
# -----------------------------
# VALIDAR LOGIN
# -----------------------------
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
@app.route("/login", methods=["POST"])
def validar():
    usuario = request.form["usuario"]
    password = request.form["password"]
<<<<<<< HEAD
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario=%s AND password=%s", (usuario, password))
    user = cursor.fetchone()
    conn.close()
    if user:
        session["user"] = usuario
        return redirect("/inicio")
    return "❌ Usuario o contraseña incorrectos"

=======

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE usuario=%s AND password=%s",
        (usuario, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        session["user"] = usuario
        return redirect("/inicio")

    return "❌ Usuario o contraseña incorrectos"

# -----------------------------
# REGISTRO
# -----------------------------
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/guardar", methods=["POST"])
def guardar_usuario():
    usuario = request.form["usuario"]
    password = request.form["password"]
<<<<<<< HEAD
    conn = conectar()
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO usuarios (usuario,password) VALUES (%s,%s)", (usuario, password))
        conn.commit()
        return redirect("/")
    except:
        return "⚠️ El usuario ya existe"
    finally:
        conn.close()

# -----------------------------
# RUTA PRINCIPAL
# -----------------------------
@app.route("/inicio")
def inicio():
    if "user" not in session:
        return redirect("/")
    
    ahora = datetime.now()
    return render_template("index.html", 
                           usuario=session["user"], 
                           fecha=ahora.strftime("%Y-%m-%d"), 
                           hora=ahora.strftime("%H:%M:%S"))

# -----------------------------
# LÓGICA DE IA (ANALIZAR)
# -----------------------------
@app.route("/analizar", methods=["POST"])
def analizar():
    if "user" not in session:
        return jsonify({"error": "No hay sesión activa"}), 401

    try:
        data = request.get_json()
        image_data = data["image"].split(";base64,")[1]
        img_bytes = base64.b64decode(image_data)
        nparr = np.frombuffer(img_bytes, np.uint8)
        img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        # Analizar con DeepFace (usamos detector_backend='opencv' por compatibilidad)
        result = DeepFace.analyze(img, actions=['emotion'], enforce_detection=False, detector_backend='opencv')
        
        emocion = result[0]["dominant_emotion"]
        consejo = consejo_emocion(emocion)

        # Guardar en BD
        conn = conectar()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO emociones (usuario, emocion) VALUES (%s, %s)", (session["user"], emocion))
        conn.commit()
        conn.close()

        return jsonify({"emotion": emocion, "advice": consejo})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/dashboard")
def dashboard():
    if "user" not in session:
        return redirect("/")
    
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT emocion, COUNT(*) FROM emociones WHERE usuario=%s GROUP BY emocion", (session["user"],))
    datos = cursor.fetchall()
    conn.close()

    conteo = {k: 0 for k in ["happy", "sad", "angry", "neutral", "fear", "surprise", "disgust"]}
=======

    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (usuario,password) VALUES (%s,%s)",
            (usuario, password)
        )
        conn.commit()
    except:
        conn.close()
        return "⚠️ El usuario ya existe"

    conn.close()
    return redirect("/")

# -----------------------------
# INICIO (AQUÍ YA ESTÁ TODO INTEGRADO)
# -----------------------------
@app.route("/inicio")
def inicio():

    if "user" not in session:
        return redirect("/")

    usuario = session["user"]

    ahora = datetime.now()
    fecha = ahora.strftime("%Y-%m-%d")
    hora = ahora.strftime("%H:%M:%S")

    return render_template(
        "index.html",
        usuario=usuario,
        fecha=fecha,
        hora=hora
    )

# -----------------------------
# ANALIZAR EMOCIÓN
# -----------------------------
@app.route("/analizar", methods=["POST"])
def analizar():

    usuario = session.get("user")
    data = request.get_json()

    image = data["image"]

    img_str = image.split(";base64,")[1]
    img_bytes = base64.b64decode(img_str)

    nparr = np.frombuffer(img_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_detector.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (255, 0, 0), 2)

    result = DeepFace.analyze(
        img,
        actions=['emotion'],
        enforce_detection=False
    )

    emocion = result[0]["dominant_emotion"]
    consejo = consejo_emocion(emocion)

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT INTO emociones (usuario,emocion) VALUES (%s,%s)",
        (usuario, emocion)
    )

    conn.commit()
    conn.close()

    return jsonify({
        "emotion": emocion,
        "advice": consejo
    })

# -----------------------------
# DASHBOARD
# -----------------------------
@app.route("/dashboard")
def dashboard():

    usuario = session.get("user")

    conn = conectar()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT emocion, COUNT(*)
        FROM emociones
        WHERE usuario=%s
        GROUP BY emocion
    """, (usuario,))

    datos = cursor.fetchall()
    conn.close()

    conteo = {
        "happy": 0,
        "sad": 0,
        "angry": 0,
        "neutral": 0,
        "fear": 0,
        "surprise": 0
    }

>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
    for emocion, cantidad in datos:
        conteo[emocion] = cantidad

    return render_template("dashboard.html", conteo=conteo)

<<<<<<< HEAD
=======
# -----------------------------
# LOGOUT
# -----------------------------
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

<<<<<<< HEAD
if __name__ == "__main__":
    app.run(debug=True)

=======
# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    app.run(debug=True)
>>>>>>> 637dd0a7d679cf6adbac26ede99b81e96f4a028c
