import os
from aura_sr import AuraSR
from PIL import Image

# Cargar el modelo AuraSR
aura_sr = AuraSR.from_pretrained(model_id="fal-ai/AuraSR", device="cpu")

# Función para cargar una imagen desde una ruta
def load_image_from_path(path):
    return Image.open(path)

# Crear directorios de salida si no existen
scaled_diff_entradas_dir = "natalia/scaled_diff_entradas"
scaled_diff_salidas_dir = "natalia/scaled_diff_salidas"
resized_dir = "natalia/resized"

os.makedirs(scaled_diff_entradas_dir, exist_ok=True)
os.makedirs(scaled_diff_salidas_dir, exist_ok=True)

# Factores de escalado para entradas y salidas
factors_entradas = {
    "120x160": 9.0, "180x240": 6.0, "240x320": 4.5, "300x400": 3.6, "360x480": 3.0,
    "480x640": 2.25, "600x800": 1.8, "720x960": 1.5, "768x1024": 1.41, "900x1200": 1.2
}
factors_salidas = [1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5, 5.5, 6, 6.5, 7, 7.5, 8, 8.5, 9, 9.5, 10]

# Proceso para scaled_diff_entradas
print("Procesando scaled_diff_entradas...")
for filename in os.listdir(resized_dir):
    if filename.endswith(".jpg"):
        input_path = os.path.join(resized_dir, filename)
        resolution = filename.split("_")[-1].split(".")[0]  # Extraer resolución, ej: '120x160'
        
        if resolution in factors_entradas:
            width, height = map(int, resolution.split("x"))  # Extraer ancho y alto del nombre
            factor = factors_entradas[resolution]
            new_width, new_height = int(width * factor), int(height * factor)
            
            image = load_image_from_path(input_path)
            upscaled_image = image.resize((new_width, new_height), Image.LANCZOS)
            
            output_path = os.path.join(scaled_diff_entradas_dir, f"{os.path.splitext(filename)[0]}_out.jpg")
            print(f"Escalando {filename} por factor {factor} → {output_path}")
            upscaled_image.save(output_path)

# Proceso para scaled_diff_salidas (Interestelar y MadMax)
print("Procesando scaled_diff_salidas...")

# Lista de imágenes a procesar
images_to_process = [
    ("natalia/resized/Interestelar_2160x2880_480x640.jpg", "Interestelar_2160x2880_480x640"),
    ("natalia/resized/MadMax_809x1200_480x640.jpg", "MadMax_809x1200_480x640")
]

for input_image_path, base_name in images_to_process:
    input_resolution = "480x640"  # La resolución base
    width, height = map(int, input_resolution.split("x"))

    for factor in factors_salidas:
        new_width, new_height = int(width * factor), int(height * factor)
        
        image = load_image_from_path(input_image_path)
        upscaled_image = image.resize((new_width, new_height), Image.LANCZOS)
        
        suffix = f"x{factor}"
        output_path = os.path.join(scaled_diff_salidas_dir, f"{base_name}_{suffix}.jpg")
        print(f"Escalando {base_name} por factor {factor} → {output_path}")
        upscaled_image.save(output_path)
