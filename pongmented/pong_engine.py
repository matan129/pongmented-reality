import numpy as np
import pygame
import pymunk
from pygame.color import *
from pygame.locals import *
from pymunk import pygame_util

from elements import *
from events import EventManager, PongEvents
from pongmented import log
from pongmented.kinect import Kinect
from sound import SoundManager


class PongEngine(object):
    """
    Runs the game!
    
    Most notably, it holds the pymunk space, which provides the physics simulation and the other game elements which
     render each frame.
     
    Also, it holds a global game state that is propagated to the elements each iteration.
    """

    def __init__(self, size, fps):
        self.max_score = 10
        self.fps = fps
        self.clock = pygame.time.Clock()
        self.running = False
        self.state = {
            'score': {
                'right': 0,
                'left': 0
            },
            'kinect': {
                'skeleton': None,
                'video': None
            },
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
        self.kinect = Kinect()

    def create_graphics(self, (w, h)):
        """
        Creates all the graphics-related members (that is, the space and elements).
        """
        log.info('Creating graphics ({}x{})', w, h)
        self.space = pymunk.Space()
        self.space.gravity = (0, 0)
        self.space.collision_bias = 0
        self.window = pygame.display.set_mode((w, h), pygame.RESIZABLE | pygame.DOUBLEBUF)
        self.pymunk_debug_draw_options = pygame_util.DrawOptions(self.window)

        self.ball = Ball(self.window, self.space, self.event_manager, (w / 2, h / 2), (0, 0))
        self.elements = [
            BackgroundDisplay(self.window, self.space, self.event_manager),
            Walls(self.window, self.space, self.event_manager),
            self.ball,
            Paddles(self.window, self.space, self.event_manager),
            ScoreDisplay(self.window, self.space, self.event_manager)
        ]
        self.ball_started = False

    def start_ball(self):
        """
        Resets the ball to the middle of the field and gives it a random starting vector.
        """
        w, h = self.window.get_size()
        random_velocity = np.random.normal(size=2)
        self.ball.set_body_params((w / 2, h / 2), random_velocity)
        self.ball_started = True

    def process_pygame_events(self):
        """
        Handles events from pygame, like key events and mouse movement.
        """
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                self.running = False
            elif event.type == VIDEORESIZE:
                if event.size != self.window.get_size():
                    self.create_graphics(event.size)

    def poll_kinect(self):
        self.state['kinect'].update(self.kinect.get_data())

    def push_state(self):
        """
        Propagates the game state to all the elements.
        """
        for element in self.elements:
            element.state = self.state

    def update_all(self):
        """
        Triggers update in all the elements.
        """
        for element in self.elements:
            element.update()

    def advance_physics(self):
        """
        Advances the simulation a little bit.
        """
        self.space.step(1.0 / self.fps)

    def process_element_events(self):
        """
        Handles events coming from elements reacting to game mechanics.
        For the time being, it's just events emitted by collision handlers.
        
        See `~elements.common.notify_hit`.
        """
        for event in self.event_manager:
            if event == PongEvents.FRAME_HIT:
                self.sound_manager.hit_sound.play()
            elif event == PongEvents.LEFT_WALL_HIT:
                self.state['score']['right'] += 1
                self.sound_manager.goal_sound.play()
                self.start_ball()
            elif event == PongEvents.RIGHT_WALL_HIT:
                self.state['score']['left'] += 1
                self.sound_manager.goal_sound.play()
                self.start_ball()
            elif event == PongEvents.BALL_PADDLE_HIT:
                self.sound_manager.hit_sound.play()
            else:
                log.warn('Unknown event: {}', event)

        self.event_manager.clear()

    def game_status(self):
        """
        Updates the game status.
        """
        left = self.state['score']['left']
        right = self.state['score']['right']
        self.state['game_over'] = left == self.max_score or right == self.max_score

    def render(self, debug):
        """
        Clears the screen and renders all the elements.
        :param debug: If true, pymunk will draw some debugging data on top of the normal render.
        """
        self.window.fill(THECOLORS['black'])

        for element in self.elements:
            element.render()

        if debug and not self.state['game_over']:
            self.space.debug_draw(self.pymunk_debug_draw_options)

        pygame.display.flip()
        pygame.display.set_caption('PONGmented Reality [FPS: {}]'.format(self.clock.get_fps()))

    def tick(self):
        """
        Makes the game advance in a constant speed.
        """
        self.clock.tick(self.fps)

    def run(self, debug_render=False):
        """
        Runs the game in a loop.
        :param debug_render: See `~render`.
        """
        log.info('Running!')
        self.running = True
        if debug_render:
            log.warn('Debug rendering is active')

        with self.kinect.activate():
            while self.running:
                self.process_pygame_events()

                if not self.running:
                    return

                if not self.ball_started:
                    self.start_ball()

                if not self.state['game_over']:
                    self.poll_kinect()
                    self.process_element_events()
                    self.game_status()
                    self.push_state()
                    self.update_all()
                    self.advance_physics()
                    self.render(debug_render)
                    self.tick()
