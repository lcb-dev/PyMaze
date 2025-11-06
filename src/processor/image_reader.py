from PIL import Image
import numpy as np
from pathlib import Path
from typing import Optional, Tuple, List

def read_image(path: Path,
               grid_size: Optional[Tuple[int,int]] = None,
               bg_percentile: float = 98.0,
               padding: int = 2,
               invert: bool = False
              ) -> Tuple[List[List[int]], Tuple[int,int]]:
    """
    Read image, crop to maze border, (optionally) resize, and return bitmap (rows of 0/1).
    1 = open/white, 0 = wall/black (unless invert=True).
    """
    p = Path(path)
    img = Image.open(p).convert("L")
    arr = np.array(img)

    th_bg = float(np.percentile(arr, bg_percentile))
    dark = arr < th_bg
    coords = np.column_stack(np.where(dark))
    if coords.size:
        y0, x0 = coords.min(axis=0)
        y1, x1 = coords.max(axis=0)
        x0 = max(x0 - padding, 0); y0 = max(y0 - padding, 0)
        x1 = min(x1 + padding, img.width - 1); y1 = min(y1 + padding, img.height - 1)
        img = Image.open(p).crop((x0, y0, x1 + 1, y1 + 1)).convert("L")

    if grid_size is not None:
        img = img.resize(grid_size, resample=Image.NEAREST)

    a = np.array(img)
    th = (int(a.min()) + int(a.max())) // 2
    bmp = (a > th).astype(np.uint8) 
    if invert:
        bmp = 1 - bmp

    pil_bitmap = Image.fromarray((bmp * 255).astype(np.uint8), mode='L')

    bitmap = bmp.tolist()
    return bitmap, (bmp.shape[1], bmp.shape[0]), pil_bitmap

