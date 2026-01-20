# Descripcion: desarrollo de una aplicacion para la deteccion facial.          
# Funcionamiento: procesamiento de los frame de la imagen
import cv2            # Libreria para el procesamiento de imagenes y video en tiempo real
import numpy as np

# Inicializacion de la camara
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

# Procesamiento continuo de los frame de entrada
while True:
    ret, frame = cap.read()
    if not ret:
        break

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
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

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

    cv2.imshow("Deteccion de caras (metodo propio)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


#“No usamos modelos preentrenados. Implementamos un sistema propio basado en procesamiento de imagen: conversión a HSV, segmentación por color de piel, detección de contornos y filtrado por tamaño y proporción para aproximar la detección de caras.”
cap.release()
cv2.destroyAllWindows()
