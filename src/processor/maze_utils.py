import numpy as np
import math
from typing import Sequence, Tuple, List
from tqdm import tqdm

def extract_edges(matrix):
    if not matrix or not matrix[0]:
        return "Empty matrix"

    rows = len(matrix)
    cols = len(matrix[0])

    top_row = matrix[0]
    bottom_row = matrix[-1]
    first_col = [row[0] for row in matrix]
    last_col = [row[-1] for row in matrix]

    return {
        "top_row": top_row,
        "first_column": first_col,
        "last_column": last_col,
        "bottom_row": bottom_row
    }

def find_entrances_old(bitmap: Sequence[Sequence[int]]) -> List[Tuple[int,int]]:
    """
    Find the two entrance/exit coordinates on the outer border of a maze.
    This currently doesn't work, because it actually ends up connecting the two entrances and considers then the same.
    """

    image_array = np.asarray(bitmap, dtype=np.uint8)
    img_height, img_width = image_array.shape

    open_mask = (image_array == 1)
    visited = np.zeros_like(open_mask, dtype=bool)
    entrances = []

    def neighbours(row, col):
        if row > 0: yield row-1, col
        if row+1 < img_height: yield row+1, col
        if col > 0: yield row, col-1
        if col+1 < img_width: yield row, col+1

    for row in tqdm(range(img_height)):
        for col in range(img_width):
            if not open_mask[row, col] or visited[row, col]:
                continue
            stack = [(row, col)]
            visited[row, col] = True
            comp = []
            touches_border = False
            border_cells = []
            while stack:
                rrow, ccol = stack.pop()
                comp.append((rrow, ccol))
                if rrow == 0 or rrow == img_height-1 or ccol == 0 or ccol == img_width-1:
                    touches_border = True
                    border_cells.append((rrow, ccol))
                for neighbour_row, neighbour_col in neighbours(rrow, ccol):
                    if open_mask[neighbour_row, neighbour_col] and not visited[neighbour_row, neighbour_col]:
                        visited[neighbour_row, neighbour_col] = True
                        stack.append((neighbour_row, neighbour_col))
            
            if touches_border:
                if len(border_cells) == 1:
                    rep_row, rep_col = border_cells[0]
                else:
                    cent_row = sum(r for r, _ in comp) / len(comp)
                    cent_col = sum(c for _, c in comp) / len(comp)

                    rep_row, rep_col = min(border_cells, key=lambda t: (t[0]-cent_row)**2 + (t[1]-cent_col)**2)
                entrances.append((rep_col, rep_row))
    
    unique = []
    for x,y in entrances:
        if (x,y) not in unique:
            unique.append((x,y))
    if len(unique) != 2:
        raise ValueError(f"Expected 2 border openings, but found: {len(unique)}: {unique}")
    return unique


def _runs_from_line(line_idx, coords):
    """Given sorted coordinate indices for one border line, return list of contiguous runs (as (start,end))."""
    if len(coords) == 0:
        return []
    runs = []
    start = coords[0]
    prev = coords[0]
    for c in coords[1:]:
        if c == prev + 1:
            prev = c
            continue
        runs.append((start, prev))
        start = c
        prev = c
    runs.append((start, prev))
    return [(line_idx, a, b) for (a, b) in runs]  # for uniform return format

def find_entrances(bitmap: Sequence[Sequence[int]]) -> List[Tuple[int,int]]:
    """
    Find entrance/exit coordinates on the outer border of a maze bitmap.
    Returns list of (x,y) coords (column,row). Tries to return exactly two points.
    """
    a = np.asarray(bitmap, dtype=np.uint8)
    h, w = a.shape
    open_mask = (a == 1)

    runs = []

    cols = np.where(open_mask[0, :])[0].tolist()
    for _, s, e in _runs_from_line(0, cols):
        runs.append(('top', s, e))

    cols = np.where(open_mask[h-1, :])[0].tolist()
    for _, s, e in _runs_from_line(h-1, cols):
        runs.append(('bottom', s, e))

    rows = np.where(open_mask[:, 0])[0].tolist()
    for _, s, e in _runs_from_line(0, rows):
        runs.append(('left', s, e))

    rows = np.where(open_mask[:, w-1])[0].tolist()
    for _, s, e in _runs_from_line(w-1, rows):
        runs.append(('right', s, e))

    points = []
    for side, s, e in runs:
        mid = (s + e) // 2
        if side == 'top':
            points.append((mid, 0))
        elif side == 'bottom':
            points.append((mid, h-1))
        elif side == 'left':
            points.append((0, mid))
        elif side == 'right':
            points.append((w-1, mid))

    uniq = []
    for p in points:
        if not any(abs(p[0]-q[0])<=1 and abs(p[1]-q[1])<=1 for q in uniq):
            uniq.append(p)

    if len(uniq) == 2:
        return uniq

    if len(uniq) < 2:
        raise ValueError(f"Expected 2 border openings, found {len(uniq)}: {uniq}")

    def dist_sq(a,b): return (a[0]-b[0])**2 + (a[1]-b[1])**2
    best_pair = None
    best_d = -1
    for i in range(len(uniq)):
        for j in range(i+1, len(uniq)):
            d = dist_sq(uniq[i], uniq[j])
            if d > best_d:
                best_d = d
                best_pair = (uniq[i], uniq[j])
    return [best_pair[0], best_pair[1]]

