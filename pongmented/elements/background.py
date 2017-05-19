import pygame
from game_object import GameObject

import cv2
import numpy as np

AREA_THRESHOLD = 200

ERODE_KERNEL = np.ones((3, 3), np.uint8)


def erode(img):
    t = cv2.erode(img, ERODE_KERNEL, iterations=1)
    return cv2.dilate(t, ERODE_KERNEL, iterations=2)


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

        im2, contours, hierarchy = cv2.findContours(g, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        img = cv2.merge((g, g, g))

        for cnt in contours:
            h = cv2.convexHull(cnt, returnPoints=False)
            area = cv2.contourArea(cv2.approxPolyDP(cnt, 0.01, True))

            if area >= AREA_THRESHOLD:
                defects = cv2.convexityDefects(cnt, h)

                if defects is not None and defects.shape:
                    for i in xrange(defects.shape[0]):
                        s, e, f, d = defects[i, 0]
                        start = tuple(cnt[s][0])
                        end = tuple(cnt[e][0])
                        cv2.line(img, start, end, [0, 255, 0], 2)

                avg = np.mean(cnt, axis=1)
                x = int(round(avg[0, 0]))
                y = int(round(avg[0, 1]))
                # cv2.putText(img, str(area), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

        # cv2.drawContours(img, contours, -1, (0, 255, 0), 3)

        surface = cv2_to_pygame(img)

        if surface:
            surface = self.state['normalizer'].surface(surface)
            surface = pygame.transform.flip(surface, True, False)
            self.window.blit(surface, (0, 0))


def cv2_to_pygame(img):
    return pygame.image.frombuffer(img.tostring(), img.shape[1::-1], 'RGB')
