# Descripcion: desarrollo de una aplicacion para la deteccion facial.          
# Funcionamiento: a traves de una interfaz grafica se muestra la imagen obtenida para la deteccion,
#                 el puerto de entrada y el numero de detecciones.
from flask import Flask, Response, render_template_string     # Libreria para la creacion del servidor web
import cv2                                                    # Libreria para el procesamiento de imagenes y video en tiempo real
import numpy as np

app = Flask(__name__)   # Generacion del servidor web

# Inicializacion del controlador de la camara
CAM_INDEX = 1  # Indice para la seleccion de la camara, en este caso solo 1

cap = cv2.VideoCapture(CAM_INDEX)
if not cap.isOpened():
    raise RuntimeError("No se pudo abrir la camara. Cambia CAM_INDEX (0/1/2).")

# Inicializacion de la interfaz del servidor web
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
    # Descripcion: procesamiento del frame para realizar la deteccion
    # Entradas: frame: contiene el frame a analizar
    # Salida: frame
    #         impresion del numero de detecciones en la interfaz web

    # Redimensionamiento del frame de entrada
    frame = cv2.resize(frame, (640, 480))

     # Conversion a HSV (Hue, Saturation, Color)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango aproximado del color de piel
    lower_skin = np.array([0, 30, 60])
    upper_skin = np.array([20, 150, 255])

    # Mascara de piel para la seleccion de aquellos pixeles que se encuentren 
    # en los posibles tonos de piel
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Filtrado del ruido del frame
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Busqueda de contornos en el frame despues de aplicar la mascara
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Almacena el numero de rostros detectados
    face_count = 0

    # Deteccion facial
    for cnt in contours:
        # Area del contorno seleccionado
        area = cv2.contourArea(cnt)

        # Descarta las areas de menor dimension
        if area < 3000:
            continue
            
        # Generacion del rectangulo en el que se encuadrara el rostro
        x, y, w, h = cv2.boundingRect(cnt)

         # Descarta los frame que no se ajusten a las dimensiones esperadas en un rostro
        ratio = h / float(w)
        if ratio < 0.9 or ratio > 1.8:
            continue

        # Aumenta el numero de deteccion
        face_count += 1

        # Actualizacion del frame 
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

    # Actualizacion del contador
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
    # Descripcion: obtencion de los frames y llamada a la funcion de procesamiento

    # Se obtienen los frames de forma continuada
    while True:
        ok, frame = cap.read()
        if not ok:
            break
            
        # Llamada a la funcion de procesamiento
        frame = process_frame(frame)

        # El frame se codifica en formato jpg para realizar el streaming
        ok, buffer = cv2.imencode(".jpg", frame)
        if not ok:
            continue
            
        # Retransmision del frame en el servidor web
        yield (b"--frame\r\n"
               b"Content-Type: image/jpeg\r\n\r\n" + buffer.tobytes() + b"\r\n")

# Seleccion de las interfaces que se mostraran segun la ruta
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
