import os
from PIL import Image

# Carpeta de origen y destino
carpeta_origen = "./"
carpeta_destino = "./imagenes_png/"

# Crea la carpeta de destino si no existe
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Lista de extensiones de archivo a convertir a PNG
extensiones_a_convertir = [".jpg", ".jpeg", ".gif", ".bmp", ".tiff"]

# Obtiene la lista de archivos en la carpeta de origen
archivos = os.listdir(carpeta_origen)

for archivo in archivos:
    if os.path.isfile(archivo):
        nombre, extension = os.path.splitext(archivo)
        extension = extension.lower()
        nuevo_nombre = nombre

        if extension in extensiones_a_convertir:
            # Abre la imagen y la convierte a PNG
            imagen = Image.open(archivo)
            nuevo_nombre = f"{nombre}.png"
            nuevo_path = os.path.join(carpeta_destino, nuevo_nombre)

            # Asegura que el nuevo nombre no exista aún
            contador = 1
            while os.path.exists(nuevo_path):
                nuevo_nombre = f"{nombre}_{contador}.png"
                nuevo_path = os.path.join(carpeta_destino, nuevo_nombre)
                contador += 1

            # Guarda la imagen en la carpeta de destino
            imagen.save(nuevo_path, "PNG")
            print(f"Convertido: {archivo} -> {nuevo_nombre}")
        elif extension == ".png":
            # Si ya es PNG, simplemente muévelo a la carpeta de destino
            nuevo_path = os.path.join(carpeta_destino, archivo)

            # Asegura que el nuevo nombre no exista aún
            contador = 1
            while os.path.exists(nuevo_path):
                nombre, _ = os.path.splitext(archivo)
                nuevo_nombre = f"{nombre}_{contador}.png"
                nuevo_path = os.path.join(carpeta_destino, nuevo_nombre)
                contador += 1

            os.rename(archivo, nuevo_path)
            print(f"Movido: {archivo} -> {nuevo_nombre}")

print("Proceso completado.")