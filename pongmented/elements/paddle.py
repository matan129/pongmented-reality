import pygame
import pymunk
from pygame.color import THECOLORS

from common import setup_elasticity, round_array, COLLISION_TYPES, constant_velocity
from game_object import GameObject


class Paddle(GameObject):
    def __init__(self, window, space):
        super(Paddle, self).__init__(window, space)
        self.radius = 60
        self.color = THECOLORS['blue']
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.velocity_func = constant_velocity(0)
        self.shape = setup_elasticity(pymunk.Circle(self.body, self.radius))
        self.shape.collision_type = COLLISION_TYPES['human_controls']
        self.space.add(self.shape, self.body)

    def update(self):
        self.body.position = self.state['mouse_position']

    def render(self):
        pygame.draw.circle(self.window, self.color, round_array(self.body.position), self.radius)
