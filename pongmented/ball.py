import numpy as np
import pygame


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
        self.pos += self.vec

    def collide_borders(self, borders):
        if self.ball is None:
            return

        if borders.top.colliderect(self.ball):
            self.vec *= np.array([1, -1])
            self.pos[1] = borders.top.y + borders.top.height + self.radius
        elif borders.bottom.colliderect(self.ball):
            self.vec *= np.array([1, -1])
            self.pos[1] = borders.bottom.y - self.radius

        if borders.left.colliderect(self.ball):
            self.vec *= np.array([-1, 1])
            self.pos[0] = borders.left.x + borders.left.width + self.radius
        elif borders.right.colliderect(self.ball):
            self.vec *= np.array([-1, 1])
            self.pos[0] = borders.right.x - self.radius
