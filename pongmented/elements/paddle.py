import pygame
import pymunk
from pygame.color import THECOLORS

from common import setup_elasticity, round_array, CollisionTypes, constant_velocity
from game_object import GameObject

OUTSIDE = (-100, -100)


class Paddle(GameObject):

    def __init__(self, window, space, event_manager, idx, radius):
        super(Paddle, self).__init__(window, space, event_manager)
        self.radius = radius
        self.idx = idx
        self.color = THECOLORS['blue']
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.velocity_func = constant_velocity(0)
        self.body.position = OUTSIDE
        self.shape = setup_elasticity(pymunk.Circle(self.body, self.radius))
        self.shape.collision_type = CollisionTypes.PADDLE
        self.space.add(self.shape, self.body)

    def update(self):
        positions = self.state['kinect']['skeleton']
        if positions is not None:
            if len(positions) > self.idx:
                position = positions[self.idx]
            else:
                position = OUTSIDE

            self.body.position = position

    def render(self):
        position = self.state['normalizer'].point(round_array(self.body.position))
        pygame.draw.circle(self.window, self.color, position, self.radius)


class Paddles(GameObject):
    def __init__(self, window, space, event_manager, limb_count=4, radius=30):
        super(Paddles, self).__init__(window, space, event_manager)
        self.p = []
        for i in xrange(limb_count):
            self.p.append(Paddle(window, space, event_manager, i, radius))

    def update(self):
        for p in self.p:
            p.state = self.state
            p.update()

    def render(self):
        for p in self.p:
            p.render()
