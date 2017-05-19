from game_object import GameObject
from pongmented import log


class BackgroundDisplay(GameObject):
    def __init__(self, window, space, event_manager):
        super(BackgroundDisplay, self).__init__(window, space, event_manager)

    def render(self):
        if not self.state['background_render']:
            return

        surface = self.state['kinect']['video']

        if surface is None:
            log.warn('Got no surface!')
            return

        if surface:
            surface = self.state['normalizer'].surface(surface)
            self.window.blit(surface, (0, 0))
