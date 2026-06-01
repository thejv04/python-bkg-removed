from rembg import remove
from PIL import Image
import io
import os


def remove_background(input_path: str, output_path: str = None) -> str:
    if not os.path.exists(input_path):
        raise FileNotFoundError(f"No se encontró el archivo: {input_path}")

    if output_path is None:
        base = os.path.splitext(input_path)[0]
        output_path = f"{base}_sin_fondo.png"

    with open(input_path, "rb") as f:
        input_data = f.read()

    output_data = remove(input_data)

    image = Image.open(io.BytesIO(output_data)).convert("RGBA")
    image.save(output_path, "PNG")

    return output_path


def get_image_preview(path: str, max_size: tuple = (400, 400)) -> Image.Image:
    img = Image.open(path)
    img.thumbnail(max_size, Image.LANCZOS)
    return img