import pygame
import numpy as np


class HumanControls(object):
    def __init__(self, window, radius, color):
        self.window = window
        self.w, self.h = window.get_size()
        self.mouse_marker = HumanMarker(window, radius, color)
        self.markers = [self.mouse_marker]

    def update(self, mouse_position):
        # TODO: Use Kinect input :)
        self.mouse_marker.update(mouse_position)

    def draw(self):
        for marker in self.markers:
            marker.draw()


class HumanMarker(object):
    def __init__(self, window, radius, color):
        self.window = window
        self.radius = radius
        self.color = color
        self.pos = None

    def update(self, pos):
        self.pos = np.array(pos)

    def draw(self):
        pygame.draw.circle(self.window, self.color, self.pos, self.radius)
