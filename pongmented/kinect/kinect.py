import contextlib
import io

import pygame
import pykinect
from PIL import Image
from pykinect.nui import ImageStreamType, ImageResolution, ImageType

from pongmented import log
from cv import detect_from_bmp

VIDEO_RESOLUTION = 640, 480


def process_frame(frame, resolution):
    image = Image.frombytes('RGBA', resolution, buffer(frame.image.bits), 'raw', 'BGRA')
    fp = io.BytesIO()
    image.save(fp, 'bmp')
    raw_image_surface = pygame.image.load_basic(io.BytesIO(fp.getvalue()))
    return raw_image_surface, detect_from_bmp(fp)


class Kinect(object):
    def __init__(self):
        self.runtime = None
        self.copies = {}

    def video_frame_ready(self, frame):
        raw_frame, (debug_frame, positions) = process_frame(frame, VIDEO_RESOLUTION)
        self.copies['raw_video'] = raw_frame.copy()
        self.copies['video'] = debug_frame.copy()
        self.copies['skeleton'] = positions.copy()

    def get_data(self):
        return self.copies.copy()

    def start(self):
        log.info('Starting Kinect...')
        self.runtime = pykinect.nui.Runtime()
        self.runtime.video_frame_ready += self.video_frame_ready
        self.runtime.video_stream.open(ImageStreamType.Video, 2, ImageResolution.Resolution640x480, ImageType.Color)

    def stop(self):
        log.info('Stopping kinect...')
        if self.runtime is not None:
            self.runtime.close()
            self.runtime = None
        else:
            log.warn('Kinect was not stopped as it was never started')

    @contextlib.contextmanager
    def activate(self):
        try:
            self.start()
            yield
        finally:
            self.stop()
