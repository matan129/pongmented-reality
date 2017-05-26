import pygame
import pymunk
from pygame.color import THECOLORS
from pymunk import Vec2d

from common import setup_elasticity, round_array, CollisionTypes, notify_hit
from game_object import GameObject
from pongmented import log
from pongmented.elements.common import constant_velocity
from pongmented.events import PongEvents


# noinspection PyUnusedLocal
def apply_player_bias(arbiter, space, data):
    """
    Pymunk CollisionHandler function.
    Makes the ball move to opponent side.
    """
    cps = arbiter.contact_point_set
    if len(cps.points) > 0:
        ball, paddle = arbiter.shapes
        bx = ball.body.position.x

        half = data['window_width'] / 2
        if bx < half:
            bias = (500, 0)
        else:
            bias = (-500, 0)

        ball.surface_velocity = bias
        arbiter.contact_point_set = cps
        ball.body.apply_impulse_at_local_point(bias)

    return True


class Ball(GameObject):
    """
    A thing that bounces.    
    """
    def __init__(self, window, space, event_manager, position, velocity):
        super(Ball, self).__init__(window, space, event_manager)
        self.radius = 25
        self.color = THECOLORS['red']
        mass = 1
        moment = pymunk.moment_for_circle(mass, 0, self.radius)
        self.body = pymunk.Body(mass, moment)
        self.body.velocity_func = constant_velocity(500)
        self.set_body_params(position, velocity)
        self.shape = setup_elasticity(pymunk.Circle(self.body, self.radius))
        self.shape.collision_type = CollisionTypes.BALL
        self.space.add(self.shape, self.body)

        handler = space.add_collision_handler(CollisionTypes.BALL, CollisionTypes.PADDLE)
        handler.begin = notify_hit
        handler.post_solve = apply_player_bias
        handler.data.update({
            'event': PongEvents.BALL_PADDLE_HIT,
            'event_manager': self.event_manager,
            'window_width': window.get_size()[0]
        })

    def set_body_params(self, position, velocity):
        self.body.position = position
        self.body.apply_impulse_at_local_point(velocity)

    def render(self):
        pygame.draw.circle(self.window, self.color, round_array(self.body.position), self.radius)
