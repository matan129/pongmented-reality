import pygame
import pymunk
from pygame.color import THECOLORS

from common import setup_elasticity, CollisionTypes
from game_object import GameObject
from pongmented.elements.common import notify_hit
from pongmented.events import PongEvents


class Walls(GameObject):
    """
    Board walls.
    """

    def __init__(self, window, space, event_manager):
        super(Walls, self).__init__(window, space, event_manager)
        self.stroke = 10
        self.color = THECOLORS['beige']
        self.walls = [
            self.create_wall((0, 0), (self.w, 0), CollisionTypes.FRAME, PongEvents.FRAME_HIT),
            self.create_wall((0, self.h), (self.w, self.h), CollisionTypes.FRAME, PongEvents.FRAME_HIT),
            self.create_wall((self.w, 0), (self.w, self.h), CollisionTypes.RIGHT_WALL, PongEvents.RIGHT_WALL_HIT),
            self.create_wall((0, 0), (0, self.h), CollisionTypes.LEFT_WALL, PongEvents.LEFT_WALL_HIT)
        ]
        self.space.add(self.walls)

    def create_wall(self, a, b, wall_collision_type, event_type):
        wall = setup_elasticity(pymunk.Segment(self.space.static_body, a, b, self.stroke))
        wall.collision_type = wall_collision_type

        handler = self.space.add_collision_handler(wall_collision_type, CollisionTypes.BALL)
        handler.begin = notify_hit
        handler.data.update({
            'event': event_type,
            'event_manager': self.event_manager
        })

        return wall

    def render(self):
        for wall in self.walls:
            pygame.draw.lines(self.window, self.color, True, [wall.a, wall.b], int(wall.radius) * 2)

        # pygame.draw.lines(self.window, self.color, True, [(self.w / 2, 0), (self.w / 2, self.h)], 20)
