import itertools as it

import numpy as np


def are_circles_colliding(a_pos, a_radius, b_pos, b_radius):
    dist = np.linalg.norm(a_pos - b_pos)
    return dist <= a_radius + b_radius


def normalize_to_unit(vec):
    return vec / magnitude(vec)


def magnitude(vec):
    return np.linalg.norm(vec)


UNIT_VECTORS = [np.array(_v) for _v in it.product([-1, 0, 1], repeat=2) if magnitude(_v) > 0]


def invert_color(color):
    inverted = []
    for v in color:
        inverted.append(255 - v)
    return tuple(inverted)


def clamp(n, min_n, man_n):
    return max(min(man_n, n), min_n)


def clamp_to_window(window, pos, margin=0):
    min_x = margin
    min_y = margin
    w, h = window.get_size()
    max_x = w - margin
    max_y = h - margin
    x = clamp(pos[0], min_x, max_x)
    y = clamp(pos[1], min_y, max_y)
    return np.array([x, y])
