from __future__ import annotations

import io
from PIL import Image, ImageEnhance, ImageOps

def apply_adjustments(
    image: Image.Image,
    *,
    brightness: float = 1.0,
    contrast: float = 1.0,
    saturation: float = 1.0,
    sharpness: float = 1.0,
    effect: str = "None",
) -> Image.Image:
    """Return a copy with non-destructive preview adjustments."""
    result = ImageOps.exif_transpose(image).convert("RGB")
    result = ImageEnhance.Brightness(result).enhance(brightness)
    result = ImageEnhance.Contrast(result).enhance(contrast)
    result = ImageEnhance.Color(result).enhance(saturation)
    result = ImageEnhance.Sharpness(result).enhance(sharpness)

    if effect == "Grayscale":
        result = ImageOps.grayscale(result).convert("RGB")
    elif effect == "Sepia":
        gray = ImageOps.grayscale(result)
        result = ImageOps.colorize(gray, black="#2b1b12", white="#f4dfb5").convert("RGB")
    return result

def image_to_png_bytes(image: Image.Image) -> bytes:
    buffer = io.BytesIO()
    image.convert("RGB").save(buffer, format="PNG", optimize=True)
    return buffer.getvalue()
