import pygame
import pymunk
from pygame.color import THECOLORS
from pygame.rect import Rect

from common import setup_elasticity, CollisionTypes
from game_object import GameObject
from pongmented.elements.common import notify_hit
from pongmented.events import PongEvents


class Walls(GameObject):
    def __init__(self, window, space, event_manager):
        super(Walls, self).__init__(window, space, event_manager)
        self.stroke = 10
        self.color = THECOLORS['lightgray']

        top = self.create_wall((0, 0), (self.w, 0), space, CollisionTypes.FRAME, PongEvents.FRAME_HIT)
        bottom = self.create_wall((0, self.h), (self.w, self.h), space, CollisionTypes.FRAME, PongEvents.FRAME_HIT)
        right = self.create_wall((self.w, 0), (self.w, self.h), space, CollisionTypes.RIGHT_WALL, PongEvents.R_HIT)
        left = self.create_wall((0, 0), (0, self.h), space, CollisionTypes.LEFT_WALL, PongEvents.L_HIT)

        self.space.add(top, bottom, right, left)
        self.walls = [
            Rect(0, 0, self.w, self.stroke),
            Rect(0, self.h - self.stroke, self.w, self.stroke),
            Rect(0, 0, self.stroke, self.h),
            Rect(self.w - self.stroke, 0, self.stroke, self.h)
        ]

    def create_wall(self, a, b, space, wall_collision_type, event_type):
        wall = setup_elasticity(pymunk.Segment(self.space.static_body, a, b, self.stroke))
        wall.collision_type = wall_collision_type

        handler = space.add_collision_handler(wall_collision_type, CollisionTypes.BALL)
        handler.begin = notify_hit
        handler.data.update({
            'event': event_type,
            'event_manager': self.event_manager
        })

        return wall

    def render(self):
        for bb_rect in self.walls:
            pygame.draw.rect(self.window, self.color, bb_rect)
