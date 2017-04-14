import enum


class EventManager(object):
    def __init__(self):
        self.events = []

    def __iter__(self):
        return iter(self.events)

    def clear(self):
        self.events = []


@enum.unique
class PongEvents(enum.IntEnum):
    L_HIT = 1
    R_HIT = 2
    FRAME_HIT = 3
