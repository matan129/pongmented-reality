import numpy as np
import pygame
from pygame.locals import *

from pongmented.players import Players


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
        self.edges = [
            (self.top, BorderInfo(Players.NO_OWNER, np.array([1, -1]))),
            (self.bottom, BorderInfo(Players.NO_OWNER, np.array([1, -1]))),
            (self.left, BorderInfo(Players.PLAYER_2, np.array([-1, 1]))),
            (self.right, BorderInfo(Players.PLAYER_1, np.array([-1, 1])))
        ]

    def draw(self):
        for edge, _ in self.edges:
            pygame.draw.rect(self.window, self.color, edge)


class BorderInfo(object):
    def __init__(self, opponent, bounce_vector):
        self.opponent = opponent
        self.bounce_vector = bounce_vector
