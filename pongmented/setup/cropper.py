import numpy as np
from pygame.color import THECOLORS

from pongmented.kinect import Kinect
import pygame
from pygame.locals import *

BLUE_VIOLET = THECOLORS['blueviolet']
MOUSE_PRIMARY = 1
MOUSE_SECONDARY = 3


class Cropper(object):
    def __init__(self, window, kinect):
        self.window = window
        self.kinect = kinect
        self.picked = False
        self.pos_primary = np.array([0, 0])
        self.pos_secondary = np.array(window.get_size())

    def pick_roi(self):
        with self.kinect.activate():
            while not self.picked:
                self.process_pygame_events()
                self.draw_kinect_image(self.window)
                self.draw_roi()
                pygame.display.flip()

            return self.pos_primary, self.pos_secondary

    def draw_roi(self):
        pygame.draw.rect(self.window, BLUE_VIOLET, Rect(self.pos_primary, self.pos_secondary - self.pos_primary), 5)

    def draw_kinect_image(self, window):
        surface = self.kinect.get_data().get("video")
        if surface:
            surface = pygame.transform.scale(surface, window.get_size())
            window.blit(surface, (0, 0))

    def process_pygame_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit(1)
                elif event.key == K_RETURN:
                    self.picked = True
            elif event.type == MOUSEBUTTONUP:
                pos = np.array(event.pos)
                if event.button == MOUSE_PRIMARY:
                    self.pos_primary = pos
                elif event.button == MOUSE_SECONDARY:
                    self.pos_secondary = pos

kinect_obj = Kinect()
a = Cropper(pygame.display.set_mode((1024, 768), pygame.RESIZABLE | pygame.DOUBLEBUF), kinect_obj)
a.pick_roi()
