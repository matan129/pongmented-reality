import pygame
from pygame.locals import *

from pongmented import log
from pongmented.ball import Ball
from pongmented.borders import Borders
from pongmented.colors import *
from pongmented.human_controls import HumanControls
from pongmented.players import Players
from pongmented.score_display import ScoreDisplay

WIDTH = 640
HEIGHT = 480
FPS = 60


class Pong(object):
    def __init__(self, width, height, fps):
        self.start_size = (width, height)
        self.window = None
        self.ball = None
        self.borders = None
        self.mouse_position = (0, 0)
        self.human_controls = None
        self.clock = pygame.time.Clock()
        self.fps = fps
        self.score = None
        self.score_display = None

    def reset(self, width, height):
        self.window = self.create_window(width, height)
        border_width = 2
        self.borders = Borders(self.window, border_width, GREEN)
        self.ball = Ball(self, (width / 4, height / border_width), 10, RED, 5.0, border_width)
        self.human_controls = HumanControls(self, border_width, 28, BLUE)
        self.score_display = ScoreDisplay(self, RED, BLUE)
        self.score = {
            Players.PLAYER_1: 0,
            Players.PLAYER_2: 0
        }

    def run_blocked(self):
        self.reset(*self.start_size)
        log.info('Running!')
        while True:
            self.clock.tick(self.fps)
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
            elif event.type == QUIT or event.type == KEYUP and event.key == K_ESCAPE:
                terminate()

    def update(self):
        self.human_controls.update()
        self.ball.update()
        for player in self.ball.last_collided:
            self.score[player] += 1

    def draw(self):
        self.window.fill(BLACK)
        self.borders.draw()
        self.ball.draw()
        self.human_controls.draw()
        self.score_display.draw()
        pygame.display.update()

    @staticmethod
    def create_window(width, height):
        log.debug('Creating window of {}x{}', width, height)
        return pygame.display.set_mode((width, height), pygame.RESIZABLE | pygame.DOUBLEBUF)


def terminate(code=0):
    log.info('Terminating')
    exit(code)


def main():
    log.info('Initializing...')
    pygame.mixer.pre_init(44100, -16, 1, 512) #Solves sound delay problems
    pygame.init()
    pygame.display.set_caption('PONGmented Reality')

    game = Pong(WIDTH, HEIGHT, FPS)
    game.run_blocked()


if __name__ == '__main__':
    main()
