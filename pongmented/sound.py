import pygame

from resources import get_resource_path


class SoundManager(object):
    """
    Responsible for loading sounds.
    """

    def __init__(self):
        self.hit_sound = pygame.mixer.Sound(get_resource_path('sounds', 'collide.wav'))
        self.goal_sound = pygame.mixer.Sound(get_resource_path('sounds', 'goal.wav'))
        self.game_over = pygame.mixer.Sound(get_resource_path('sounds', 'game_over.wav'))
