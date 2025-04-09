import os
from pathlib import Path

from pyodm import Node

# Configuraciones
base_path = os.path.dirname(os.path.abspath(__file__))
print(f"[INFO] Ruta base: {base_path}")
IMAGES_DIR = Path(os.path.join(base_path, "images"))
OUTPUT_DIR = Path(os.path.join(base_path, "results"))
NODE_URL = "http://localhost:3000"


def main():
    print(f"[INFO] Conectando a nodo en {NODE_URL}...")
    node = Node("localhost", 3000)

    image_files = [str(p) for p in IMAGES_DIR.glob("*.jpeg")]
    if not image_files:
        print("[WARN] No se encontraron imágenes JPG en la carpeta:", IMAGES_DIR)
        return

    print(f"[INFO] Subiendo {len(image_files)} imágenes para procesar...")

    task = node.create_task(
        image_files,
        options={
            "dsm": True,
            "pc-quality": "high",
            "orthophoto-resolution": 5,
            "gcp": str(Path(base_path) / "gcp_list.txt"),
        },
    )

    print("[INFO] Procesando... ")
    task.wait_for_completion()
    print("[SUCCESS] Procesamiento completado")

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    print(f"[INFO] Descargando resultados en {OUTPUT_DIR}...")
    task.download_assets(str(OUTPUT_DIR))

    print("[SUCCESS] Todo listo. Resultados descargados.")


if __name__ == "__main__":
    main()
