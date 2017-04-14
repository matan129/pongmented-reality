import numpy as np
import enum


@enum.unique
class CollisionTypes(enum.IntEnum):
    BALL = 0
    FRAME = 1
    RIGHT_WALL = 2
    LEFT_WALL = 3
    PADDLE = 4


def setup_elasticity(shape):
    shape.friction = 0.0
    shape.elasticity = 1.0
    return shape


def round_array(arr):
    return np.array(arr).round().astype(int)


def constant_velocity(speed):
    def _constant_velocity(body, gravity, damping, dt):
        body.velocity = body.velocity.normalized() * speed
    return _constant_velocity


def notify_hit(arbiter, space, data):
    event = data['event']
    event_manager = data['event_manager']
    event_manager.events.append(event)
    return True