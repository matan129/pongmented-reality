import pygame
from pygame.locals import *

from utils import *


class Ball(object):
    def __init__(self, window, position, radius, ball_color):
        self.window = window
        self.pos = np.array(position)
        self.vec = np.array([1, 1])
        self.radius = radius
        self.color = ball_color
        self.ball = None

    def draw(self):
        self.ball = pygame.draw.circle(self.window, self.color, self.pos, self.radius)

    def update(self):
        self.pos += np.rint(self.vec).astype(int)

    def collide_borders(self, borders):
        if self.ball is None:
            return

        if borders.top.colliderect(self.ball):
            self.vec *= np.array([1, -1])
            self.uncollide_rect(borders.top)
        elif borders.bottom.colliderect(self.ball):
            self.vec *= np.array([1, -1])
            self.uncollide_rect(borders.bottom)

        if borders.left.colliderect(self.ball):
            self.vec *= np.array([-1, 1])
            self.uncollide_rect(borders.left)
        elif borders.right.colliderect(self.ball):
            self.vec *= np.array([-1, 1])
            self.uncollide_rect(borders.right)

    def uncollide_rect(self, rect):
        bounding_rect = None
        while not bounding_rect or rect.colliderect(bounding_rect):
            self.update()
            bounding_rect = Rect(self.pos - np.array([self.radius, self.radius]), (self.radius * 2, self.radius * 2))

    def collide_human_controls(self, human_controls):
        if self.ball is None:
            return

        for marker in human_controls.markers:
            if are_circles_colliding(self.pos, self.radius, marker.pos, marker.radius):
                self.vec = normalize_to_unit(self.pos - marker.pos)
                self.uncollide_circle(marker.pos, marker.radius)

    def uncollide_circle(self, pos, radius):
        while are_circles_colliding(self.pos, self.radius, pos, radius):
            self.update()
