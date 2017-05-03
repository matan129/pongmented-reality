import pygame
import pymunk
from pygame.color import THECOLORS
from pykinect.nui import JointId

from common import setup_elasticity, round_array, CollisionTypes, constant_velocity
from game_object import GameObject
from pykinect.nui import SkeletonEngine

OUTSIDE = (-100, -100)


class Paddle(GameObject):
    """
    Mouse-controlled paddle.
    """
    def __init__(self, window, space, event_manager, idx, joint):
        super(Paddle, self).__init__(window, space, event_manager)
        self.joint = joint
        self.radius = 80
        self.color = THECOLORS['blue']
        self.body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.body.velocity_func = constant_velocity(0)
        self.body.position = OUTSIDE
        self.shape = setup_elasticity(pymunk.Circle(self.body, self.radius))
        self.shape.collision_type = CollisionTypes.PADDLE
        self.player_idx = idx
        self.space.add(self.shape, self.body)

    def flip_x(self, (x, y)):
        return self.w - x, y

    def update(self):
        skeleton = self.state['kinect']['skeleton']
        if skeleton is not None:
            player = skeleton[self.player_idx]
            joint = player.SkeletonPositions[self.joint]
            kinect_position = SkeletonEngine.skeleton_to_depth_image(joint, self.w, self.h)
            position = self.flip_x(kinect_position)

            if position[0] <= 0 and position[1] <= 0:
                position = OUTSIDE

            self.body.position = position

    def render(self):
        pygame.draw.circle(self.window, self.color, self.state['normalizer'].point(round_array(self.body.position)), self.radius)


class Paddles(GameObject):
    def __init__(self, window, space, event_manager, player_count=6):
        super(Paddles, self).__init__(window, space, event_manager)
        self.p = [Paddle(window, space, event_manager, i, JointId.HandLeft) for i in xrange(player_count)]

    def update(self):
        for p in self.p:
            p.state = self.state
            p.update()

    def render(self):
        for p in self.p:
            p.render()
