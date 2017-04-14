import enum


class EventManager(object):
    """
    Small class that decouples event processing from event emitting.
    Basically, elements put events in and the engine takes them out.
    """
    def __init__(self):
        self.events = []

    def __iter__(self):
        return iter(self.events)

    def clear(self):
        self.events = []


@enum.unique
class PongEvents(enum.IntEnum):
    LEFT_WALL_HIT = 1
    RIGHT_WALL_HIT = 2
    FRAME_HIT = 3
    BALL_PADDLE_HIT = 4
