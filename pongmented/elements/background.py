import pygame
from game_object import GameObject


class BackgroundDisplay(GameObject):
    def __init__(self, window, space, event_manager):
        super(BackgroundDisplay, self).__init__(window, space, event_manager)

    def render(self):
        return
        surface = self.state['kinect']['video']
        if surface:
            surface = self.state['normalizer'].surface(surface)
            surface = pygame.transform.flip(surface, True, False)
            self.window.blit(surface, (0, 0))
