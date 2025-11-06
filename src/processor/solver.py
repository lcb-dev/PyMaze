from collections import deque
from typing import Sequence, Tuple, List, Optional
from PIL import Image, ImageDraw
import numpy as np

Coord = Tuple[int,int]

def draw_path_on_image(pil_img: Image.Image,
                       path: Sequence[Coord],
                       out_path: str = "solved.png",
                       width: int = 3,
                       line_color: Tuple[int,int,int] = (255,0,0)) -> None:
    """
    Draw `path` (sequence of (x,y) pixel coordinates) as a continuous colored line onto `pil_img`
    and save to `out_path`. Accepts grayscale or RGB PIL image; it will convert to RGB.
    """
    if len(path) == 0:
        raise ValueError("empty path")
    img = pil_img.convert("RGB")
    draw = ImageDraw.Draw(img)
    draw.line(path, fill=line_color, width=width)
    ex, ey = path[-1]; sx, sy = path[0]
    r = max(1, width+1)
    draw.ellipse((sx-r, sy-r, sx+r, sy+r), outline=(0,255,0))
    draw.ellipse((ex-r, ey-r, ex+r, ey+r), outline=(0,0,255))
    img.save(out_path)