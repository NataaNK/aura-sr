from aura_sr import AuraSR

aura_sr = AuraSR.from_pretrained(model_id="fal-ai/AuraSR", device="cpu")

import requests
from io import BytesIO
from PIL import Image

def load_image_from_url(url):
    response = requests.get(url)
    image_data = BytesIO(response.content)
    return Image.open(image_data)

from PIL import Image

def load_image_from_path(path):
    return Image.open(path)


image = load_image_from_path("natalia/resized/Interestelar_2160x2880_120x160.jpg").resize()
upscaled_image = aura_sr.upscale_4x(image)

# Guarda la imagen superresolucionada
upscaled_image.save("natalia/scaled/output_2.jpg")

