import pygame
from pygame.color import THECOLORS
from pygame.rect import Rect

from pongmented.resources import get_resource_path
from game_object import GameObject


class ScoreDisplay(GameObject):
    """
    Displays the score on the board.
    Also displays some info after the game is over.
    """

    def __init__(self, window, space, event_manager):
        super(ScoreDisplay, self).__init__(window, space, event_manager)
        self.color = THECOLORS['beige']
        self.w, self.h = window.get_size()
        self.score_font = pygame.font.Font(get_resource_path('fonts', 'pong_score.ttf'), self.h / 16)
        self.text_font = pygame.font.SysFont('consolas', self.h / 6)
        self.winner_font = pygame.font.SysFont('consolas', self.h / 8)

    def render(self):
        if self.state['game_over']:
            self.render_game_over()
        else:
            self.render_score()

    def render_score(self):
        left_label = self.score_font.render(str(self.state['score']['left']), True, self.color)
        ll_w, _ = left_label.get_size()
        score_height = self.h / 10
        base_x = self.w / 8
        self.window.blit(left_label, (base_x - ll_w / 2, score_height))
        right_label = self.score_font.render(str(self.state['score']['right']), True, self.color)
        rl_w, _ = right_label.get_size()
        self.window.blit(right_label, (7 * base_x - rl_w / 2, score_height))

    def render_game_over(self):
        self.window.fill(THECOLORS['black'])
        left_winner = self.state['score']['left'] > self.state['score']['right']

        rect_start = (self.w / 2, 0) if not left_winner else (0, 0)
        pygame.draw.rect(self.window, THECOLORS['gold'], Rect(rect_start, (self.w / 2, self.h)))

        game_over_label = self.text_font.render('Game Over', True, THECOLORS['red2'])
        self.window.blit(game_over_label, (self.w / 2 - game_over_label.get_size()[0] / 2, self.h / 4))

        winner_label = self.winner_font.render('Winner!', True, THECOLORS['white'])

        winner_w = winner_label.get_size()[0]
        winner_x = 3 * self.w if not left_winner else self.w
        winner_x = winner_x / 4 - winner_w / 2
        self.window.blit(winner_label, (winner_x, 3 * self.h / 4))
