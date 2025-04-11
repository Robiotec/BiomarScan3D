import os

# Ruta de la carpeta con las imágenes
carpeta_imagenes = "/home/ose/Documents/BiomarScan3D/scripts/images"

# Obtener una lista de archivos en la carpeta
archivos = os.listdir(carpeta_imagenes)

# Filtrar solo los archivos de imagen (por extensión)
extensiones_validas = (".jpg", ".jpeg", ".png", ".bmp", ".gif")
imagenes = [archivo for archivo in archivos if archivo.lower().endswith(extensiones_validas)]

# Renombrar las imágenes
for i, imagen in enumerate(imagenes, start=1):
    # Obtener la extensión del archivo
    extension = os.path.splitext(imagen)[1]
    # Crear el nuevo nombre
    nuevo_nombre = f"imagen_{i}{extension}"
    # Ruta completa de los archivos
    ruta_actual = os.path.join(carpeta_imagenes, imagen)
    nueva_ruta = os.path.join(carpeta_imagenes, nuevo_nombre)
    # Renombrar el archivo
    os.rename(ruta_actual, nueva_ruta)

print("✅ Imágenes renombradas correctamente.")
