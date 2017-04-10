import pygame
from pygame.locals import *

from pongmented import log
from pongmented.ball import Ball
from pongmented.borders import Borders

BLACK = pygame.color.THECOLORS['black']
WHITE = pygame.color.THECOLORS['white']
RED = pygame.color.THECOLORS['red']
GREEN = pygame.color.THECOLORS['green']

WIDTH = 640
HEIGHT = 480


class Pong(object):
    def __init__(self):
        self.window = None
        self.ball = None
        self.borders = None
        self.hands = None
        self.mouse_position = None
        self.load(WIDTH, HEIGHT)

    def load(self, width, height):
        self.window = self.create_window(width, height)
        self.ball = Ball(self.window, (width / 4, height / 2), 10, RED)
        self.borders = Borders(self.window, 2, GREEN)
        self.hands = None  # TODO

    def run(self):
        while True:
            pygame.time.delay(1)
            self.process_events()
            self.update()
            self.draw()

    def process_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)
            elif event.type == MOUSEMOTION:
                self.mouse_position = event.pos
            elif event.type == VIDEORESIZE:
                if self.window.get_size() != (event.w, event.h):
                    self.load(event.w, event.h)

    def update(self):
        self.ball.update()
        self.ball.collide_borders(self.borders)

    def draw(self):
        self.window.fill(BLACK)
        self.borders.draw()
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

    log.info('Running!')
    game = Pong()
    game.run()


if __name__ == '__main__':
    main()
