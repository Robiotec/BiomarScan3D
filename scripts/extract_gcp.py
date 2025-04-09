import math
from pathlib import Path

import cv2

# Configuración
IMAGES_DIR = Path("scripts/images")
OUTPUT_DIR = Path("scripts/gcp_detected_preview")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_TXT = Path("scripts/gcp_list.txt")

# Coordenadas simuladas por forma
forma_a_coord = {
    "triángulo": (0, 0, 0),
    "cuadrado": (20, 0, 0),
    "cruz": (0, 20, 0),
    "círculo": (20, 20, 0),
}


def detectar_gcps(img, filename):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 🎯 Rango personalizado para bolígrafo morado
    lower_color = (163, 111, 0)
    upper_color = (180, 255, 255)
    mask = cv2.inRange(hsv, lower_color, upper_color)

    # Suavizado y limpieza
    blur = cv2.GaussianBlur(mask, (9, 9), 0)
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
    clean = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel, iterations=1)

    # Contornos
    contours, _ = cv2.findContours(clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    detecciones = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < 500 or area > 9000:
            continue

        perimeter = cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, 0.03 * perimeter, True)
        vertices = len(approx)
        x, y, w, h = cv2.boundingRect(cnt)
        aspect_ratio = w / float(h)
        bounding_area = w * h
        ratio = area / bounding_area
        circularity = 4 * math.pi * area / (perimeter * perimeter)

        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        shape = "desconocido"
        color = (0, 0, 0)

        print(
            f"🔍 Detección: {vertices} vértices, área: {area}, relación de aspecto: {aspect_ratio:.2f}, circularidad: {circularity:.2f}"
        )

        if vertices < 7 and circularity <= 0.75:
            shape = "triángulo"
            color = (0, 255, 255)
        elif (vertices == 4 or vertices == 5) and 0.80 <= aspect_ratio <= 1.08:
            shape = "cuadrado"
            color = (0, 255, 0)
        elif 0.80 <= circularity <= 1.2:
            shape = "círculo"
            color = (0, 0, 255)
        elif 6 <= vertices <= 20 and ratio < 0.6:
            shape = "cruz"
            color = (255, 255, 0)

        if shape != "desconocido":
            cv2.drawContours(img, [cnt], -1, color, 2)
            cv2.circle(img, (cx, cy), 5, (255, 255, 255), -1)
            cv2.putText(
                img, shape, (cx + 10, cy), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2
            )
            detecciones.append(
                {"shape": shape, "filename": filename, "cx": cx, "cy": cy}
            )

    return img, detecciones


def main():
    all_detecciones = []

    for file in IMAGES_DIR.glob("*.jpeg"):
        print(f"📷 Procesando: {file.name}")
        img = cv2.imread(str(file))
        if img is None:
            print(f"❌ No se pudo cargar {file.name}")
            continue

        salida, dets = detectar_gcps(img, file.name)
        all_detecciones.extend(dets)
        cv2.imwrite(str(OUTPUT_DIR / file.name), salida)

    # Exportar gcp_list.txt
    with open(OUTPUT_TXT, "w") as f:
        for d in all_detecciones:
            if d["shape"] in forma_a_coord:
                x, y, z = forma_a_coord[d["shape"]]
                f.write(f"EPSG:0,{x},{y},{z},{d['filename']},{d['cx']},{d['cy']}\n")
                f.write(f"{x} {y} {z} {d['cx']} {d['cy']} {d['filename']}\n")

    print("✅ Detección completada.")
    print(f"📄 Archivo generado: {OUTPUT_TXT}")
    print(f"🖼️ Previsualizaciones guardadas en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
