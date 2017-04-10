import pygame
from pygame.locals import *
import numpy as np


class Borders(object):
    def __init__(self, window, stroke, border_color):
        self.window = window
        self.color = border_color
        self.stroke = stroke
        w, h = self.window.get_size()
        self.top = Rect(0, 0, w, stroke)
        self.bottom = Rect(0, h - stroke, w, stroke)
        self.right = Rect(w - stroke, 0, stroke, h)
        self.left = Rect(0, 0, stroke, h)
        self.edges_to_vectors = [
            (self.top, np.array([1, -1])),
            (self.bottom, np.array([1, -1])),
            (self.left, np.array([-1, 1])),
            (self.right, np.array([-1, 1]))
        ]

    def draw(self):
        for edge, _ in self.edges_to_vectors:
            pygame.draw.rect(self.window, self.color, edge)
