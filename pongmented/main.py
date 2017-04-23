import pygame
from pymunk import pygame_util

from pong_engine import PongEngine
from pongmented import log


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
    game = PongEngine((1024, 768), 60)
    game.run(debug_render=False)


if __name__ == '__main__':
    main()
