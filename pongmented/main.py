import sys
import click
import ctypes
import pygame
from pymunk import pygame_util

from pong_engine import PongEngine
from pongmented import log


def setup_pygame():
    ctypes.windll.user32.SetProcessDPIAware()
    pygame.mixer.pre_init(44100, -16, 1, 512)  # Solves sound delay problems
    pygame.init()
    pygame.display.set_caption('PONGmented Reality')


def setup_pymunk():
    pygame_util.positive_y_is_up = False  # Makes the pymunk and pygame axis systems the same


@click.command()
@click.option('--width', '-w', default=1024, help='Screen width')
@click.option('--height', '-h', default=768, help='Screen height')
@click.option('--fps', '-f', default=30, help='FPS')
@click.option('--debug-render', '-d', default=False, help='Enable Pymunk debug rendering', is_flag=True)
@click.option('--background-render', '-b', default=False, help='Enable rendering the captured video', is_flag=True)
@click.option('--sound/--no-sound', default=True, help='Enable/disable in-game sound')
@click.option('--max-score', '-m', default=4, help='The max game score')
@click.option('--slowdown', '-s', default=1.0, help='Slowdown coefficient')
def main(width, height, fps, debug_render, background_render, sound, max_score, slowdown):
    log.info('Starting...')
    setup_pygame()
    setup_pymunk()
    game = PongEngine((width, height), fps, max_score, debug_render, background_render, sound, slowdown)
    game.run()


if __name__ == '__main__':
    main(sys.argv[1:])
