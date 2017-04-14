import pygame

from resources import get_resource_path


class SoundManager(object):
    def __init__(self):
        self.hit_sound = pygame.mixer.Sound(get_resource_path('sounds', 'collide.wav'))
        self.goal_sound = pygame.mixer.Sound(get_resource_path('sounds', 'goal.wav'))
