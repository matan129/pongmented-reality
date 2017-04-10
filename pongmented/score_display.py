import pygame

from pongmented.players import Players


class ScoreDisplay(object):
    def __init__(self, game, player1_color, player2_color):
        self.game = game
        self.w, self.h = game.window.get_size()
        self.font = pygame.font.SysFont('consolas', self.h / 8)
        self.player1_color = player1_color
        self.player2_color = player2_color

    def draw(self):
        p1_label = self.font.render(str(self.game.score[Players.PLAYER_1]), True, self.player1_color)
        self.game.window.blit(p1_label, (self.w / 4, self.h / 4))

        p2_label = self.font.render(str(self.game.score[Players.PLAYER_2]), True, self.player2_color)
        self.game.window.blit(p2_label, (3 * self.w / 4, self.h / 4))
