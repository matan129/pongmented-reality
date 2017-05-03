import pygame
from pygame.locals import *


class CoordinateNormalizer(object):
    def __init__(self, pos1, pos2, width, height):
        self.pos1 = pos1
        self.pos2 = pos2
        self.w = width
        self.h = height

    def surface(self, surface):
        scaled = pygame.transform.scale(surface, (self.w, self.h))
        cropped = scaled.subsurface(Rect(self.pos1, self.pos2 - self.pos1))
        return pygame.transform.scale(cropped, (self.w, self.h))

    def point(self, point):
        off_x = point[0] - self.pos1[0]
        ratio_x = self.w / (self.pos2[0] - self.pos1[0])
        norm_x = int(off_x * ratio_x)

        off_y = point[1] - self.pos1[1]
        ratio_y = self.h / (self.pos2[1] - self.pos1[1])
        norm_y = int(off_y * ratio_y)
        return norm_x, norm_y
