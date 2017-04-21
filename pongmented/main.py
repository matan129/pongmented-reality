import pygame
import sys
from pymunk import pygame_util

import logbook
from pongmented import log
from pong_engine import PongEngine


def setup_pygame():
    pygame.mixer.pre_init(44100, -16, 1, 512)  # Solves sound delay problems
    pygame.init()
    pygame.display.set_caption('PONGmented Reality')


def setup_pymunk():
    pygame_util.positive_y_is_up = False  # Makes the pymunk and pygame axis systems the same


def main():
    log.info('Starting...')
    setup_pygame()
    setup_pymunk()
    game = PongEngine((1600, 800), 120)
    game.run(debug_render=False)


if __name__ == '__main__':
    with logbook.StreamHandler(sys.stdout).applicationbound():
        main()
