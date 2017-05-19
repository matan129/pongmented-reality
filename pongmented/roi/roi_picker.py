import numpy as np
from coordinate_normalizer import CoordinateNormalizer
from pygame.color import THECOLORS
import pygame
from pygame.locals import *

BLUE_VIOLET = THECOLORS['blueviolet']
MOUSE_PRIMARY = 1
MOUSE_SECONDARY = 3


class RoiPicker(object):
    def __init__(self, window, kinect):
        self.window = window
        self.window_size = window.get_size()
        self.kinect = kinect
        self.picked = False
        self.pos_primary = None
        self.pos_secondary = None
        self.kinect_surface = None
        self.toggle_display = True
        self.reset_pos()

    def reset_pos(self):
        self.pos_primary = np.array([0, 0], dtype=np.float)
        self.pos_secondary = np.array(self.window_size, dtype=np.float)

    def pick(self):
        while not self.picked:
            self.display_initial()

            if self.kinect_surface:
                self.window.blit(self.kinect_surface, (0, 0))

            self.process_pygame_events()
            self.draw_roi()
            pygame.display.flip()

        return CoordinateNormalizer(self.pos_primary, (640, 480), *self.window_size)

    def display_initial(self):
        self.window.fill(THECOLORS['green'])

    def draw_roi(self):
        pygame.draw.rect(self.window, BLUE_VIOLET, Rect(self.pos_primary, self.pos_secondary - self.pos_primary), 5)

    def acquire_kinect_image(self):
        surface = None
        while not surface:
            surface = self.kinect.get_data().get('raw_video')

        self.fix_kinect_surface(surface)

    def fix_kinect_surface(self, surface):
        surface = pygame.transform.scale(surface, self.window_size)
        surface = pygame.transform.flip(surface, True, False)
        self.kinect_surface = surface

    def process_pygame_events(self):
        for event in pygame.event.get():
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    exit(1)
                elif event.key == K_RETURN:
                    self.picked = True
                elif event.key == K_SPACE:
                    if self.toggle_display:
                        self.acquire_kinect_image()
                        self.toggle_display = False
                    else:
                        self.display_initial()
                        self.kinect_surface = None
                        self.toggle_display = True
            elif event.type == MOUSEBUTTONUP:
                pos = np.array(event.pos, dtype=np.float)
                if event.button == MOUSE_PRIMARY:
                    self.pos_primary = pos
                elif event.button == MOUSE_SECONDARY:
                    self.pos_secondary = pos
            elif event.type == VIDEORESIZE:
                self.window_size = event.size
                self.reset_pos()

                if self.kinect_surface:
                    self.fix_kinect_surface(self.kinect_surface)
