import pygame
from pygame.color import THECOLORS

from pongmented.resources import get_resource_path
from game_object import GameObject


class ScoreDisplay(GameObject):
    """
    Displays the score on the board.
    Also displays some info after the game is over.
    """

    def __init__(self, window, space, event_manager):
        super(ScoreDisplay, self).__init__(window, space, event_manager)
        self.color = THECOLORS['lightgray']
        self.w, self.h = window.get_size()
        self.score_font = pygame.font.Font(get_resource_path('fonts', 'pong_score.ttf'), self.h / 8)
        self.text_font = pygame.font.SysFont('consolas', self.h / 4)

    def render(self):
        if self.state['game_over']:
            self.render_game_over()
        else:
            self.render_score()

    def render_score(self):
        left_label = self.score_font.render(str(self.state['score']['left']), True, self.color)
        ll_w, _ = left_label.get_size()
        self.window.blit(left_label, (self.w / 4 - ll_w / 2, self.h / 4))
        right_label = self.score_font.render(str(self.state['score']['right']), True, self.color)
        rl_w, _ = right_label.get_size()
        self.window.blit(right_label, (3 * self.w / 4 - rl_w / 2, self.h / 4))

    def render_game_over(self):
        self.window.fill(THECOLORS['black'])
        game_over_label = self.text_font.render('Game Over!', True, THECOLORS['red2'])
        self.window.blit(game_over_label, (self.w / 2 - game_over_label.get_size()[0] / 2, self.h / 4))
        left_winner = self.state['score']['left'] > self.state['score']['right']
        winner_text = '<--- Winner' if left_winner else 'Winner --->'
        winner_label = self.text_font.render(winner_text, True, THECOLORS['gold'])
        self.window.blit(winner_label, (self.w / 2 - winner_label.get_size()[0] / 2, 3 * self.h / 4))
