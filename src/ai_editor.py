from __future__ import annotations

import base64
import io
from openai import OpenAI
from PIL import Image

ALLOWED_MODELS = {
    "gpt-image-2.5-sunburst",
    "gpt-image-2.5-flare",
}

def edit_image(*, image_bytes: bytes, prompt: str, api_key: str, model: str) -> bytes:
    """Call OpenAI's image-edit endpoint and return PNG bytes."""
    if model not in ALLOWED_MODELS:
        raise ValueError("Unsupported image model.")
    if not prompt.strip():
        raise ValueError("Edit instructions cannot be empty.")
    if len(image_bytes) > 20 * 1024 * 1024:
        raise ValueError("Image exceeds the 20 MB application limit.")

    client = OpenAI(api_key=api_key)
    response = client.images.edit(
        model=model,
        image=("source.png", io.BytesIO(image_bytes), "image/png"),
        prompt=prompt,
        output_format="png",
    )
    encoded = response.data[0].b64_json
    if not encoded:
        raise RuntimeError("The image API returned no image data.")
    output = base64.b64decode(encoded)
    # Validate that the API response is a readable image before returning it.
    with Image.open(io.BytesIO(output)) as image:
        image.verify()
    return output
