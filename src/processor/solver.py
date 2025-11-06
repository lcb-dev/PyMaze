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

def bfs_path(
    bitmap: Sequence[Sequence[int]], 
    start: Coord,
    end: Coord) -> List[Coord]:
    """
    Breadth first search!
    Find shortest path from start to finish on a grid, where 1=0 and 0=wall
    """

    maze_array = np.asarray(bitmap, dtype=np.uint8)
    maze_height, maze_width = maze_array.shape

    start_x, start_y = start
    end_x, end_y = end

    if not (
        0 <= start_x < maze_width 
        and 0 <= start_y < maze_height 
        and 0 <= end_x < maze_width 
        and 0 <= end_y < maze_height):
        raise ValueError("Start/end out of bounds!")
    if maze_array[start_y,start_x] == 0 or maze_array[end_y,end_x] == 0:
        raise ValueError("Start or end is on a wall!")

    maze_q = deque()
    maze_q.append((start_x,start_y))
    prev = { (start_x, start_y): None }

    while maze_q:
        x,y = maze_q.popleft()
        if (x, y) == (end_x, end_y):
            path = []
            cur = (x, y)
            while cur is not None:
                path.append(cur)
                cur = prev[cur]
            path.reverse()
            return path
        
        for nx, ny in ((x-1,y),(x+1,y),(x,y-1),(x,y+1)):
            if 0 <= nx < maze_width and 0 <= ny < maze_height and maze_array[ny, nx] == 1 and (nx, ny) not in prev:
                prev[(nx, ny)] = (x, y)
                maze_q.append((nx, ny))
    raise ValueError("No path found between start and end")