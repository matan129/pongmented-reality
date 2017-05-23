import numpy as np
from coordinate_normalizer import CoordinateNormalizer
from pygame.color import THECOLORS
import pygame
from pygame.locals import *
import os
import json
from pongmented import log

CONF_DIR = os.path.join(os.getenv('LOCALAPPDATA'), 'pongmented')

BLUE_VIOLET = THECOLORS['blueviolet']
MOUSE_PRIMARY = 1
MOUSE_SECONDARY = 3


class RoiPicker(object):

    CONF_FILE = os.path.join(CONF_DIR, 'roi.json')

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

        if os.path.exists(self.CONF_FILE):
            self.load_settings()

        if self.window_size != self.window.get_size():
            self.window = pygame.display.set_mode(self.window_size, pygame.RESIZABLE | pygame.DOUBLEBUF)

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

        self.persist_settings()

        return CoordinateNormalizer(self.pos_primary, self.pos_secondary, *self.window_size)

    def persist_settings(self):
        with open(self.CONF_FILE, 'w') as f:
            json.dump({
                'primary': tuple(self.pos_primary),
                'secondary': tuple(self.pos_secondary),
                'window_size': tuple(self.window_size)
            }, f)

    def load_settings(self):
        try:
            with open(self.CONF_FILE) as f:
                d = json.load(f)
                pos_primary = np.array(d['primary'])
                pos_secondary = np.array(d['secondary'])
                window_size = np.array(d['window_size'])
                self.pos_primary = pos_primary
                self.pos_secondary = pos_secondary
                self.window_size = window_size
        except (ValueError, KeyError):
            log.exception('Skipping ROI restoration')

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
