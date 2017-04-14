import pygame
import pymunk
from pygame.color import THECOLORS

from common import setup_elasticity, round_array
from game_object import GameObject
from pongmented.elements.common import constant_velocity


class Ball(GameObject):
    def __init__(self, window, space, position, velocity):
        super(Ball, self).__init__(window, space)
        self.radius = 15
        self.color = THECOLORS['red']
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)
        self.body.velocity_func = constant_velocity(500)
        self.set_body_params(position, velocity)
        self.shape = setup_elasticity(pymunk.Circle(self.body, self.radius))
        self.space.add(self.shape, self.body)

    def set_body_params(self, position, velocity):
        self.body.position = position
        self.body.velocity = velocity
        self.body.apply_impulse_at_local_point(velocity)

    def render(self):
        pygame.draw.circle(self.window, self.color, round_array(self.body.position), self.radius)
