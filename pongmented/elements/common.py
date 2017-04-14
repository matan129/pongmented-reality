import numpy as np

COLLISION_TYPES = {name: i for i, name in enumerate([
    'ball',
    'frame',
    'right_wall',
    'left_wall',
    'human_controls'
])}


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
