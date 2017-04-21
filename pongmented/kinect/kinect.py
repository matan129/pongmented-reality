import contextlib
import io

import pygame
import pykinect
from PIL import Image
from pykinect.nui import JointId, ImageStreamType, ImageResolution, ImageType

from pongmented import log
from pongmented.kinect.double_buffer import DoubleBuffer

VIDEO_RESOLUTION = 640, 480


LEFT_ARM = (JointId.ShoulderCenter,
            JointId.ShoulderLeft,
            JointId.ElbowLeft,
            JointId.WristLeft,
            JointId.HandLeft)

RIGHT_ARM = (JointId.ShoulderCenter,
             JointId.ShoulderRight,
             JointId.ElbowRight,
             JointId.WristRight,
             JointId.HandRight)

LEFT_LEG = (JointId.HipCenter,
            JointId.HipLeft,
            JointId.KneeLeft,
            JointId.AnkleLeft,
            JointId.FootLeft)

RIGHT_LEG = (JointId.HipCenter,
             JointId.HipRight,
             JointId.KneeRight,
             JointId.AnkleRight,
             JointId.FootRight)

SPINE = (JointId.HipCenter,
         JointId.Spine,
         JointId.ShoulderCenter,
         JointId.Head)


def image_from_frame(frame, resolution):
    image = Image.frombytes('RGBA', resolution, buffer(frame.image.bits), 'raw', 'BGRA')
    fp = io.BytesIO()
    image.save(fp, 'bmp')
    return pygame.image.load_basic(io.BytesIO(fp.getvalue()))


class Kinect(object):
    def __init__(self):
        self.runtime = None
        self.double_buffer = DoubleBuffer(True, ['video', 'skeleton'])

    def video_frame_ready(self, frame):
        self.double_buffer['video'] = image_from_frame(frame, VIDEO_RESOLUTION)

    def post_skeleton(self, frame):
        self.double_buffer['skeleton'] = frame.SkeletonData

    def get_data(self):
        return self.double_buffer.get_all()

    def start(self):
        log.info('Starting Kinect...')
        self.runtime = pykinect.nui.Runtime()
        self.runtime.skeleton_engine.enabled = True
        self.runtime.skeleton_frame_ready += self.post_skeleton
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