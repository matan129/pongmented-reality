import pygame
import pymunk
from pygame.color import *
from pygame.locals import *
from pymunk import pygame_util

from elements import *
from events import EventManager, PongEvents
from pongmented import log
from sound import SoundManager
from utils import random_unit_vector


class PongEngine(object):
    def __init__(self, size, fps):
        self.max_score = 8
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = False
        self.state = {
            'score': {
                'right': 0,
                'left': 0
            },
            'mouse_position': (0, 0),
            'game_over': False
        }

        self.ball_started = False
        self.space = None
        self.window = None
        self.elements = None
        self.pymunk_debug_draw_options = None
        self.ball = None
        self.event_manager = EventManager()
        self.sound_manager = SoundManager()
        self.create_graphics(size)

    def create_graphics(self, (w, h)):
        log.info('Creating graphics ({}x{})', w, h)
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.space.collision_bias = 0
        self.window = pygame.display.set_mode((w, h), pygame.RESIZABLE | pygame.DOUBLEBUF)
        self.pymunk_debug_draw_options = pygame_util.DrawOptions(self.window)

        self.ball = Ball(self.window, self.space, self.event_manager, (w / 2, h / 2), (0, 0))
        self.elements = [
            Walls(self.window, self.space, self.event_manager),
            self.ball,
            Paddle(self.window, self.space, self.event_manager),
            ScoreDisplay(self.window, self.space, self.event_manager)
        ]
        self.ball_started = False

    def start_ball(self):
        w, h = self.window.get_size()
        self.ball.set_body_params((w / 2, h / 2), random_unit_vector())
        self.ball_started = True

    def point_to_pygame(self, point):
        return pygame_util.to_pygame(point, self.window)

    def process_pygame_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = False
            elif event.type == MOUSEMOTION:
                self.state['mouse_position'] = self.point_to_pygame(event.pos)
            elif event.type == VIDEORESIZE:
                if event.size != self.window.get_size():
                    self.create_graphics(event.size)

    def push_state(self):
        for element in self.elements:
            element.state = self.state

    def update_all(self):
        for element in self.elements:
            element.update()

    def advance_physics(self):
        self.space.step(1.0 / self.fps)

    def process_element_events(self):
        for event in self.event_manager:
            if event == PongEvents.FRAME_HIT:
                self.sound_manager.hit_sound.play()
            elif event == PongEvents.L_HIT:
                self.state['score']['right'] += 1
                self.sound_manager.goal_sound.play()
                self.start_ball()
            elif event == PongEvents.R_HIT:
                self.state['score']['left'] += 1
                self.sound_manager.goal_sound.play()
                self.start_ball()
            elif event == PongEvents.BALL_PADDLE_HIT:
                self.sound_manager.hit_sound.play()
            else:
                log.warn('Unknown event: {}', event)

        self.event_manager.clear()

    def game_status(self):
        self.state['game_over'] = self.state['score']['left'] == self.max_score \
                                  or self.state['score']['right'] == self.max_score

    def render(self, debug):
        self.window.fill(THECOLORS['black'])

        for element in self.elements:
            element.render()

        if debug:
            self.space.debug_draw(self.pymunk_debug_draw_options)

        pygame.display.flip()
        pygame.display.set_caption('PONGmented Reality [FPS: {}]'.format(self.clock.get_fps()))

    def tick(self):
        self.clock.tick(self.fps)

    def run(self, debug_render=False):
        log.info('Running!')
        self.running = True

        if debug_render:
            log.warn('Debug rendering is active')

        while self.running:
            self.process_pygame_events()

            if not self.running:
                return

            if not self.ball_started:
                self.start_ball()

            if not self.state['game_over']:
                self.process_element_events()
                self.game_status()
                self.push_state()
                self.update_all()
                self.advance_physics()
                self.render(debug_render)
                self.tick()
