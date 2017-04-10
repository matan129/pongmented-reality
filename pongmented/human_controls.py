import pygame
import numpy as np

from pongmented.utils import invert_color, clamp_to_window


class HumanControls(object):
    def __init__(self, game, margin, radius, color):
        self.game = game
        self.mouse_marker = HumanMarker(game, margin, radius, color, 'M1')
        self.markers = [self.mouse_marker]

    def update(self):
        # TODO: Use Kinect input :)
        self.mouse_marker.update(self.game.mouse_position)

    def draw(self):
        for marker in self.markers:
            marker.draw()


class HumanMarker(object):
    def __init__(self, game, margin, radius, color, label=None):
        self.game = game
        self.margin = margin
        self.radius = radius
        self.color = color
        self.pos = None

        if label:
            font = pygame.font.SysFont('consolas', radius)
            self.label = font.render(label, True, invert_color(color))
        else:
            self.label = None

    def update(self, pos):
        self.pos = clamp_to_window(self.game.window, pos, self.radius + self.margin)

    def draw(self):
        pygame.draw.circle(self.game.window, self.color, self.pos, self.radius)
        if self.label:
            self.game.window.blit(self.label, self.pos - (np.array([self.radius, self.radius]) / 2))
