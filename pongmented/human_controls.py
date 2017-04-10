import pygame
import numpy as np

from pongmented.utils import clamp, invert_color


class HumanControls(object):
    def __init__(self, window, margin, radius, color):
        self.window = window
        self.mouse_marker = HumanMarker(window, margin, radius, color, 'M1')
        self.markers = [self.mouse_marker]

    def update(self, mouse_position):
        # TODO: Use Kinect input :)
        self.mouse_marker.update(mouse_position)

    def draw(self):
        for marker in self.markers:
            marker.draw()


class HumanMarker(object):
    def __init__(self, window, margin, radius, color, label=None):
        self.window = window
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
        self.pos = np.array(self.clamp_position(pos))

    def clamp_position(self, pos):
        min_x = self.radius + self.margin
        min_y = self.radius + self.margin
        w, h = self.window.get_size()
        max_x = w - self.radius - self.margin
        max_y = h - self.radius - self.margin
        x = clamp(pos[0], min_x, max_x)
        y = clamp(pos[1], min_y, max_y)
        return np.array([x, y])

    def draw(self):
        pygame.draw.circle(self.window, self.color, self.pos, self.radius)
        if self.label:
            self.window.blit(self.label, self.pos - (np.array([self.radius, self.radius]) / 2))
