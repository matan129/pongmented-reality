import pygame
from pygame.rect import Rect


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

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.top)
        pygame.draw.rect(self.window, self.color, self.bottom)
        pygame.draw.rect(self.window, self.color, self.left)
        pygame.draw.rect(self.window, self.color, self.right)
