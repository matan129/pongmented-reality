import numpy as np
from pymunk import pygame_util


def magnitude(vec):
    return np.linalg.norm(vec)


def normalize_to_unit(vec):
    return vec / magnitude(vec)


def random_unit_vector(dims=2):
    return normalize_to_unit(np.random.normal(size=dims))


def point_to_pygame(window, point):
    return pygame_util.to_pygame(point, window)
