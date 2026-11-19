from PIL import Image
from src.image_ops import apply_adjustments, image_to_png_bytes

def test_adjustments_return_rgb_image():
    source = Image.new("RGB", (32, 24), (120, 80, 40))
    result = apply_adjustments(source, brightness=1.1, effect="Sepia")
    assert result.mode == "RGB"
    assert result.size == (32, 24)

def test_png_export_is_valid():
    source = Image.new("RGB", (10, 10), "red")
    data = image_to_png_bytes(source)
    assert data.startswith(b"\\x89PNG\\r\\n\\x1a\\n")
