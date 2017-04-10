import numpy as np


def are_circles_colliding(a_pos, a_radius, b_pos, b_radius):
    dist = np.linalg.norm(a_pos - b_pos)
    return dist <= a_radius + b_radius


def normalize_to_unit(vec):
    magnitude = np.linalg.norm(vec)
    return vec / magnitude
