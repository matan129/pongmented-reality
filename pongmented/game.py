import pygame
from pygame.locals import *
import numpy as np
import time

from pongmented import log

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

WIDTH = 600
HEIGHT = 400


class Borders(object):
    def __init__(self, window, stroke=2, border_color=GREEN):
        self.window = window
        self.color = border_color
        self.stroke = stroke
        w, h = self.window.get_size()
        self.top = Rect(0, 0, w, stroke)
        self.bottom = Rect(0, h - stroke, w, stroke)
        self.right = Rect(w - stroke, 0, stroke, h)
        self.left = Rect(0, 0, stroke, h)

    def draw(self):
        pygame.draw.rect(self.window, self.color, self.top)
        pygame.draw.rect(self.window, self.color, self.bottom)
        pygame.draw.rect(self.window, self.color, self.left)
        pygame.draw.rect(self.window, self.color, self.right)


class Ball(object):

    def __init__(self, window, position, radius=10, ball_color=RED):
        self.window = window
        self.pos = np.array(position)
        self.vec = np.array([1, 1])
        self.radius = radius
        self.color = ball_color
        self.ball = pygame.draw.circle(self.window, self.color, self.pos, self.radius)

    def draw(self):
        self.ball = pygame.draw.circle(self.window, self.color, self.pos, self.radius)

    def update(self):
        self.pos += self.vec

    def collide_borders(self, borders):
        if borders.top.colliderect(self.ball):
            self.vec *= np.array([1, -1])
            self.pos[1] = borders.top.y + borders.top.height + self.radius
        elif borders.bottom.colliderect(self.ball):
            self.vec *= np.array([1, -1])
            self.pos[1] = borders.bottom.y - self.radius

        if borders.left.colliderect(self.ball):
            self.vec *= np.array([-1, 1])
            self.pos[0] = borders.left.x + borders.left.width + self.radius
        elif borders.right.colliderect(self.ball):
            self.vec *= np.array([-1, 1])
            self.pos[0] = borders.right.x - self.radius


class Pong(object):

    def __init__(self):
        self.mouse_position = (WIDTH/2, HEIGHT/2)
        self.window = pygame.display.set_mode((WIDTH, HEIGHT), 0, 32)
        self.ball = Ball(self.window, (WIDTH/4, HEIGHT/2))
        self.borders = Borders(self.window)
        self.hands = None

    def run(self):
        while True:
            self.tick()
            self.draw()

    def draw(self):
        self.window.fill(BLACK)
        self.borders.draw()
        self.ball.draw()
        pygame.display.update()

    def draw_hands(self):
        self.hands["hand1"] = pygame.draw.circle(self.window, RED, self.mouse_position, 15)

    def update(self):
        self.ball.update()
        self.ball.collide_borders(self.borders)

    def tick(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                exit(0)
            elif event.type == MOUSEMOTION:
                self.mouse_position = event.pos

        time.sleep(0.01)
        self.update()


def main():
    log.info('Starting...')
    pygame.init()
    pygame.display.set_caption('PONGmented Reality')

    game = Pong()
    game.run()


if __name__ == '__main__':
    main()
