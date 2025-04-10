from pathlib import Path

import cv2

# Configuración
IMAGES_DIR = Path("scripts/images")
OUTPUT_DIR = Path("scripts/gcp_detected_preview")
OUTPUT_DIR.mkdir(exist_ok=True)
OUTPUT_TXT = Path("scripts/gcp_list.txt")

# Coordenadas simuladas por color
color_a_coord = {
    "azul": (0, 0, 0),
    "rojo": (20, 0, 0),
    "negro": (0, 20, 0),
}


def detectar_gcps(img, filename):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 🎯 Rango HSV para cada color
    color_ranges = {
        "azul": {
            "lower": (0, 195, 157),
            "upper": (128, 255, 255),
            "bgr": (255, 0, 0),
        },
        "rojo": {
            "lower": (148, 77, 0),
            "upper": (180, 255, 255),
            "bgr": (0, 0, 255),
        },
        "negro": {
            "lower": (63, 0, 0),
            "upper": (169, 255, 62),
            "bgr": (50, 50, 50),
        },
    }

    detecciones = []

    for color_name, params in color_ranges.items():
        mask = cv2.inRange(hsv, params["lower"], params["upper"])

        blur = cv2.GaussianBlur(mask, (9, 9), 0)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
        clean = cv2.morphologyEx(blur, cv2.MORPH_CLOSE, kernel, iterations=1)

        contours, _ = cv2.findContours(
            clean, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if color_name == "azul":
                if area < 1100 or area > 30000:
                    continue
            elif color_name == "rojo":
                if area < 7000 or area > 30000:
                    continue
            else:
                if area < 4000 or area > 30000:
                    continue

            M = cv2.moments(cnt)
            if M["m00"] == 0:
                continue
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])

            cv2.drawContours(img, [cnt], -1, params["bgr"], 2)
            cv2.circle(img, (cx, cy), 5, (255, 255, 255), -1)
            cv2.putText(
                img,
                color_name,
                (cx + 10, cy),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                params["bgr"],
                2,
            )

            detecciones.append(
                {"color": color_name, "filename": filename, "cx": cx, "cy": cy}
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

    with open(OUTPUT_TXT, "w") as f:
        f.write(
            "+proj=utm +zone=10 +ellps=WGS84 +datum=WGS84 +units=m +no_defs\n"
        )  # Header para WebODM
        for d in all_detecciones:
            if d["color"] in color_a_coord:
                x, y, z = color_a_coord[d["color"]]
                f.write(f"{x} {y} {z} {d['cx']} {d['cy']} {d['filename']}\n")

    print("✅ Detección completada.")
    print(f"📄 Archivo generado: {OUTPUT_TXT}")
    print(f"🖼️ Previsualizaciones guardadas en: {OUTPUT_DIR}")


if __name__ == "__main__":
    main()
