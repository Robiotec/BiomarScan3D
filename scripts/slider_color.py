import cv2
import numpy as np
from pathlib import Path

IMG_DIR = Path("scripts/images")

def nothing(x):
    pass

def main():
    # Obtener todas las imágenes
    image_paths = list(IMG_DIR.glob("*.jpeg"))
    if not image_paths:
        print("❌ No hay imágenes .jpeg en la carpeta.")
        return

    current_img_index = 0
    img = cv2.imread(str(image_paths[current_img_index]))
    img = cv2.resize(img, (800, 600))  # escala para visualización
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Crear ventana con sliders
    cv2.namedWindow("Adjust HSV")

    cv2.createTrackbar("H Min", "Adjust HSV", 0, 180, nothing)
    cv2.createTrackbar("H Max", "Adjust HSV", 180, 180, nothing)
    cv2.createTrackbar("S Min", "Adjust HSV", 0, 255, nothing)
    cv2.createTrackbar("S Max", "Adjust HSV", 255, 255, nothing)
    cv2.createTrackbar("V Min", "Adjust HSV", 0, 255, nothing)
    cv2.createTrackbar("V Max", "Adjust HSV", 255, 255, nothing)

    print("🎚️ Controles:")
    print("'q' para salir")
    print("'n' siguiente imagen")
    print("'p' imagen anterior")

    while True:
        # Leer valores del slider
        h_min = cv2.getTrackbarPos("H Min", "Adjust HSV")
        h_max = cv2.getTrackbarPos("H Max", "Adjust HSV")
        s_min = cv2.getTrackbarPos("S Min", "Adjust HSV")
        s_max = cv2.getTrackbarPos("S Max", "Adjust HSV")
        v_min = cv2.getTrackbarPos("V Min", "Adjust HSV")
        v_max = cv2.getTrackbarPos("V Max", "Adjust HSV")

        # Crear máscara
        lower = np.array([h_min, s_min, v_min])
        upper = np.array([h_max, s_max, v_max])
        mask = cv2.inRange(hsv, lower, upper)

        # Mostrar imagen original y máscara
        result = cv2.bitwise_and(img, img, mask=mask)
        cv2.imshow("Original", img)
        cv2.imshow("Mask", mask)
        cv2.imshow("Filtrado", result)

        key = cv2.waitKey(1)
        if key == ord("q"):
            print(f"\n🎯 Rango HSV ajustado:")
            print(f"Lower: {lower}")
            print(f"Upper: {upper}")
            break
        elif key == ord("n"):  # siguiente imagen
            current_img_index = (current_img_index + 1) % len(image_paths)
            img = cv2.imread(str(image_paths[current_img_index]))
            img = cv2.resize(img, (800, 600))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            print(f"\n📸 Imagen actual: {image_paths[current_img_index].name}")
        elif key == ord("p"):  # imagen anterior
            current_img_index = (current_img_index - 1) % len(image_paths)
            img = cv2.imread(str(image_paths[current_img_index]))
            img = cv2.resize(img, (800, 600))
            hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
            print(f"\n📸 Imagen actual: {image_paths[current_img_index].name}")

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
