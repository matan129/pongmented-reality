import pygame
from pygame.locals import *

from pongmented import log
from pongmented.players import Players
from utils import *


class Ball(object):
    def __init__(self, game, position, radius, ball_color, speed_multiplier, margin):
        self.game = game
        self.pos = np.array(position)
        self.vec = random_unit_vector()
        self.radius = radius
        self.color = ball_color
        self.speed_multiplier = speed_multiplier
        self.margin = margin
        self.bounding_rect = None
        self.last_collided = None

    def update(self):
        self.last_collided = []
        self.advance_pos()
        self.collide_human_controls()
        self.collide_borders()
        self.pos = clamp_to_window(self.game.window, self.pos, self.radius + self.margin)

    def advance_pos(self):
        self.pos += self.vec.dot(self.speed_multiplier).round().astype(int)
        self.bounding_rect = Rect(self.pos - np.repeat([self.radius], 2), np.repeat([self.radius * 2], 2))

    def collide_borders(self):
        for edge, info in self.game.borders.edges:
            if edge.colliderect(self.bounding_rect):
                if info.opponent != Players.NO_OWNER:
                    self.last_collided.append(info.opponent)
                self.vec *= info.bounce_vector
                self.uncollide_rect(edge)

    def collide_human_controls(self):
        for marker in self.game.human_controls.markers:
            if are_circles_colliding(self.pos, self.radius, marker.pos, marker.radius):
                self.vec = normalize_to_unit(self.pos - marker.pos)
                self.uncollide_circle(marker.pos, marker.radius)

    def uncollide_rect(self, rect):
        while rect.colliderect(self.bounding_rect):
            self.advance_pos()

    def uncollide_circle(self, pos, radius):
        while are_circles_colliding(self.pos, self.radius, pos, radius):
            self.advance_pos()

    def draw(self):
        log.trace('Ball pos: {}', self.pos)
        pygame.draw.circle(self.game.window, self.color, self.pos, self.radius)
