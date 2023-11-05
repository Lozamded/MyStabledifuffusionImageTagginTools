import os

# Carpeta de origen donde se encuentran las imágenes PNG
carpeta_origen = "./imagenes_png/"

# Carpeta de destino para los archivos de texto
carpeta_destino = "./archivos_txt/"

# Crea la carpeta de destino si no existe
if not os.path.exists(carpeta_destino):
    os.makedirs(carpeta_destino)

# Texto específico que se agregará a cada archivo de texto
texto_especifico = "Nombre del personaje,"

# Obtiene la lista de archivos PNG en la carpeta de origen
archivos_png = [archivo for archivo in os.listdir(carpeta_origen) if archivo.endswith(".png")]

for archivo_png in archivos_png:
    # Crea el nombre del archivo de texto basado en el nombre de la imagen PNG
    nombre_txt = os.path.splitext(archivo_png)[0] + ".txt"
    ruta_txt = os.path.join(carpeta_destino, nombre_txt)

    # Abre el archivo de texto en modo escritura y agrega el texto específico
    with open(ruta_txt, "w") as archivo_txt:
        archivo_txt.write(texto_especifico)

    print(f"Creado archivo de texto: {nombre_txt}")

print("Proceso completado.")