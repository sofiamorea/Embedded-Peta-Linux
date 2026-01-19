import cv2
import numpy as np

# Abrir cámara USB (cambia 0/1/2 si hace falta)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("No se pudo abrir la cámara")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Redimensionar para estabilidad
    frame = cv2.resize(frame, (640, 480))

    # Convertir a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Rango aproximado de color de piel
    lower_skin = np.array([0, 30, 60])
    upper_skin = np.array([20, 150, 255])

    # Máscara de piel
    mask = cv2.inRange(hsv, lower_skin, upper_skin)

    # Limpiar ruido
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    mask = cv2.erode(mask, kernel, iterations=2)
    mask = cv2.dilate(mask, kernel, iterations=2)

    # Buscar contornos
    contours, _ = cv2.findContours(
        mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    face_count = 0

    for cnt in contours:
        area = cv2.contourArea(cnt)

        # Filtrar objetos pequeños
        if area < 3000:
            continue

        x, y, w, h = cv2.boundingRect(cnt)

        # Filtro de proporción (cara ≈ rectángulo vertical)
        ratio = h / float(w)
        if ratio < 0.9 or ratio > 1.8:
            continue

        face_count += 1

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

    cv2.imshow("Deteccion de caras (metodo propio)", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break


#“No usamos modelos preentrenados. Implementamos un sistema propio basado en procesamiento de imagen: conversión a HSV, segmentación por color de piel, detección de contornos y filtrado por tamaño y proporción para aproximar la detección de caras.”
cap.release()
cv2.destroyAllWindows()
