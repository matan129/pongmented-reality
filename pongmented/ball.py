import random

import pygame
from pygame.locals import *

from pongmented import log
from utils import *


class Ball(object):
    def __init__(self, window, position, radius, ball_color):
        self.window = window
        self.pos = np.array(position)
        self.vec = random.choice(UNIT_VECTORS)
        self.radius = radius
        self.color = ball_color
        self.bounding_rect = None

    def update(self):
        self.pos += np.rint(self.vec).astype(int)
        self.bounding_rect = Rect(self.pos - np.array([self.radius, self.radius]), (self.radius * 2, self.radius * 2))

    def draw(self):
        log.trace('Ball pos: {}', self.pos)
        pygame.draw.circle(self.window, self.color, self.pos, self.radius)

    def collide_borders(self, borders):
        for edge, bounce_vector in borders.edges_to_vectors:
            if edge.colliderect(self.bounding_rect):
                self.vec *= bounce_vector
                self.uncollide_rect(edge)

    def collide_human_controls(self, human_controls):
        for marker in human_controls.markers:
            if are_circles_colliding(self.pos, self.radius, marker.pos, marker.radius):
                self.vec = normalize_to_unit(self.pos - marker.pos)
                self.uncollide_circle(marker.pos, marker.radius)

    def uncollide_rect(self, rect):
        while rect.colliderect(self.bounding_rect):
            self.update()

    def uncollide_circle(self, pos, radius):
        while are_circles_colliding(self.pos, self.radius, pos, radius):
            self.update()
