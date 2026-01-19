from flask import Flask, Response, render_template_string
import cv2
import numpy as np

app = Flask(__name__)

CAM_INDEX = 1  # tu camara USB (cambia 0/1/2 si hace falta)

cap = cv2.VideoCapture(CAM_INDEX)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la camara. Cambia CAM_INDEX (0/1/2).")

PAGE = """
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Deteccion de caras (metodo propio)</title>
    <style>
      body { font-family: Arial; margin: 20px; background: #fafafa; }
      .card { max-width: 980px; border: 1px solid #ddd; background: white;
              border-radius: 12px; padding: 14px; }
      img { width: 100%; height: auto; border-radius: 12px; }
      .note { color: #555; }
      code { background: #f1f1f1; padding: 2px 6px; border-radius: 6px; }
    </style>
  </head>
  <body>
    <div class="card">
      <h2>Streaming + Deteccion de caras (metodo propio)</h2>
      <p class="note">
        Procesamiento: HSV → mascara piel → morfologia → contornos → filtros tamaño/proporcion.
        Salida en <code>/video_feed</code>. Pulsa <code>Ctrl+C</code> en la terminal para parar.
      </p>
      <img src="/video_feed">
    </div>
  </body>
</html>
"""

def process_frame(frame):
    # Redimensionar para estabilidad (igual que tu codigo)
    frame = cv2.resize(frame, (640, 480))

    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango aproximado de color de piel
    lower_skin = np.array([0, 30, 60])
    upper_skin = np.array([20, 150, 255])

    # Mascara de piel
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Limpiar ruido
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Buscar contornos
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    face_count = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Filtrar objetos pequeños
        if area < 3000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        # Filtro de proporcion
        ratio = h / float(w)
        if ratio < 0.9 or ratio > 1.8:
            continue

        face_count += 1

        # Rectangulo + etiqueta
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(
            frame,
            f"Objeto detectado: Cara {face_count}",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2
        )

    # Texto superior
    cv2.putText(
        frame,
        f"Caras detectadas: {face_count}",
        (10, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        1,
        (255, 0, 0),
        2
    )

    return frame

def gen_frames():
    while True:
        ok, frame = cap.read()
        if not ok:
            break

        frame = process_frame(frame)

        # Codificar a JPEG para streaming
        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            continue

        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

@app.route("/")
def index():
    return render_template_string(PAGE)

@app.route("/video_feed")
def video_feed():
    return Response(gen_frames(),
                    mimetype="multipart/x-mixed-replace; boundary=frame")

if __name__ == "__main__":
    # 0.0.0.0 => accesible desde otros dispositivos en la misma red
    app.run(host="0.0.0.0", port=5000, debug=False, threaded=True)
