import numpy as np
import enum


@enum.unique
class CollisionTypes(enum.IntEnum):
    """
    Collision types are used to differentiate pymunk object collision events, so a unique handler can be assigned for 
    collision between the ball and the paddle (but not the ball and a wall), for instance.
    """
    BALL = 0
    FRAME = 1
    RIGHT_WALL = 2
    LEFT_WALL = 3
    PADDLE = 4


def setup_elasticity(shape):
    """
    Makes everything perfect :)
    """
    shape.friction = 0.0
    shape.elasticity = 1.0
    return shape


def round_array(arr):
    return np.array(arr).round().astype(int)


def constant_velocity(speed):
    """
    :param speed: The magnitude.
    :return: A function that is useful as velocity_func in pymunk.
             This function can be used to keep the velocity of a given pymunk body constant.
             For example, see `~Ball.__init__`.
    """
    def _constant_velocity(body, gravity, damping, dt):
        """
        Normalizes a given velocity vector to the given magnitude.
        """
        body.velocity = body.velocity.normalized() * speed
    return _constant_velocity


def notify_hit(arbiter, space, data):
    """
    This is a pymunk CollisionHandler function.
    Used to enqueue and event after a collision has started.
    See `~Walls.create_wall`.
    For more information, see `http://www.pymunk.org/en/latest/pymunk.html#pymunk.CollisionHandler.begin`.
    """
    event = data['event']
    event_manager = data['event_manager']
    event_manager.events.append(event)
    return True
