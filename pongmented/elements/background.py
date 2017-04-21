import pygame
from game_object import GameObject


class BackgroundDisplay(GameObject):
    def __init__(self, window, space, event_manager):
        super(BackgroundDisplay, self).__init__(window, space, event_manager)

    def render(self):
        surface = self.state['kinect']['video']
        if surface:
            surface = pygame.transform.scale(surface, (self.w, self.h))
            self.window.blit(surface, (0, 0))
