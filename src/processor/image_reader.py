from PIL import Image
import numpy as np
from pathlib import Path

def read_image(image: Path):
    with Image.open(image) as img:
        width, height = img.size
        print(f"Image height: {height}")
        print(f"Image width: {width}")
    return None

