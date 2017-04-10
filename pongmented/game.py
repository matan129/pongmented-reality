from pygame.locals import *

from pongmented import log
from pongmented.ball import Ball
from pongmented.borders import Borders
from pongmented.colors import *
from pongmented.human_controls import HumanControls

WIDTH = 640
HEIGHT = 480


class Pong(object):
    def __init__(self, width, height):
        self.window = None
        self.ball = None
        self.borders = None
        self.mouse_position = None
        self.human_controls = None
        self.reset(width, height)

    def reset(self, width, height):
        self.window = self.create_window(width, height)
        self.ball = Ball(self.window, (width / 4, height / 2), 10, RED)
        self.borders = Borders(self.window, 2, GREEN)
        self.human_controls = HumanControls(self.window, 2, 28, BLUE)

    def run(self):
        log.info('Running!')
        while True:
            pygame.time.delay(3)
            self.process_events()
            self.update()
            self.draw()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == MOUSEMOTION:
                log.trace('Mouse pos: {}',  event.pos)
                self.mouse_position = event.pos
            elif event.type == VIDEORESIZE:
                if self.window.get_size() != (event.w, event.h):
                    self.reset(event.w, event.h)
            elif event.type == QUIT:
                exit(0)

    def update(self):
        self.human_controls.update(self.mouse_position)
        self.ball.update()
        self.ball.collide_human_controls(self.human_controls)
        self.ball.collide_borders(self.borders)

    def draw(self):
        self.window.fill(BLACK)
        self.borders.draw()
        self.human_controls.draw()
        self.ball.draw()
        pygame.display.update()

    @staticmethod
    def create_window(width, height):
        log.debug('Creating window of {}x{}', width, height)
        return pygame.display.set_mode((width, height), pygame.RESIZABLE)


def main():
    log.info('Initializing...')
    pygame.init()
    pygame.display.set_caption('PONGmented Reality')

    game = Pong(WIDTH, HEIGHT)
    game.run()


if __name__ == '__main__':
    main()
