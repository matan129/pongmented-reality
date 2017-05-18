import pygame
from game_object import GameObject

import cv2
import numpy as np


ERODE_KERNEL = np.ones((5,5), np.uint8)


def erode(img):
    t = cv2.erode(img, ERODE_KERNEL, iterations=1)
    return cv2.dilate(t, ERODE_KERNEL, iterations=1)


class BackgroundDisplay(GameObject):
    def __init__(self, window, space, event_manager):
        super(BackgroundDisplay, self).__init__(window, space, event_manager)

    def render(self):
        if not self.state['background_render']:
            return

        img = self.state['kinect']['video']

        if img is None:
            return

        r, g, b = cv2.split(img)
        _, r = cv2.threshold(r, 220, 255, cv2.THRESH_BINARY)
        _, g = cv2.threshold(g, 220, 255, cv2.THRESH_BINARY)
        _, b = cv2.threshold(b, 220, 255, cv2.THRESH_BINARY)

        br = cv2.bitwise_or(r, b)
        br = cv2.bitwise_not(br)
        g = cv2.bitwise_and(br, g)

        g = erode(g)

        img = cv2.merge((g, g, g))
        surface = cv2_to_pygame(img)

        if surface:
            surface = self.state['normalizer'].surface(surface)
            surface = pygame.transform.flip(surface, True, False)
            self.window.blit(surface, (0, 0))


def cv2_to_pygame(img):
    return pygame.image.frombuffer(img.tostring(), img.shape[1::-1], 'RGB')
