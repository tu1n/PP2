import pygame
from collections import deque

# flood fill эт заливка как в пэйнт
def flood_fill(surface, x, y, new_color):
    old_color = surface.get_at((x, y))[:3]
    
    if old_color == new_color[:3]:
        return

    queue = deque()
    queue.append((x, y))

    w = surface.get_width()
    h = surface.get_height()

    while queue:
        px, py = queue.popleft()

        if px < 0 or px >= w or py < 0 or py >= h:
            continue

        if surface.get_at((px, py))[:3] != old_color:
            continue

        surface.set_at((px, py), new_color)

        queue.append((px + 1, py))
        queue.append((px - 1, py))
        queue.append((px, py + 1))
        queue.append((px, py - 1))