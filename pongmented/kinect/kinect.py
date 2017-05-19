import contextlib
import io

import pygame
import pykinect
from PIL import Image
from pykinect.nui import JointId, ImageStreamType, ImageResolution, ImageType

from pongmented import log
from pongmented.kinect.double_buffer import DoubleBuffer

import cv2
import numpy as np

MIN_THRESH = 220

MAX_BRIGHTNESS = 255

VIDEO_RESOLUTION = 640, 480
AREA_THRESHOLD = 180
ERODE_KERNEL = np.ones((3, 3), np.uint8)


def reduce_noise(img):
    t = cv2.erode(img, ERODE_KERNEL, iterations=1)
    return cv2.dilate(t, ERODE_KERNEL, iterations=2)


def detect(img):
    r, g, b = cv2.split(img)
    _, r = cv2.threshold(r, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)
    _, g = cv2.threshold(g, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)
    _, b = cv2.threshold(b, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)

    br = cv2.bitwise_or(r, b)
    br = cv2.bitwise_not(br)
    g = cv2.bitwise_and(br, g)

    g = reduce_noise(g)

    im2, contours, hierarchy = cv2.findContours(g, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    img = cv2.merge((g, g, g))

    positions = []
    for cnt in contours:
        h = cv2.convexHull(cnt, returnPoints=False)
        area = cv2.contourArea(cv2.approxPolyDP(cnt, 0.01, True))

        if area >= AREA_THRESHOLD:
            defects = cv2.convexityDefects(cnt, h)

            if defects is not None and defects.shape:
                for i in xrange(defects.shape[0]):
                    s, e, f, d = defects[i, 0]
                    start = tuple(cnt[s][0])
                    end = tuple(cnt[e][0])
                    cv2.line(img, start, end, [0, MAX_BRIGHTNESS, 0], 2)

            avg = np.mean(cnt, axis=1)
            x = int(round(avg[0, 0]))
            y = int(round(avg[0, 1]))
            positions.append((x, y))
            # cv2.putText(img, str(area), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, 255)

    # cv2.drawContours(img, contours, -1, (0, 255, 0), 3)
    return cv2_to_pygame(img), positions


def process_frame(frame, resolution):
    image = Image.frombytes('RGBA', resolution, buffer(frame.image.bits), 'raw', 'BGRA')
    fp = io.BytesIO()
    image.save(fp, 'bmp')
    return detect(cv2.flip(cv2_decode(to_array(fp)), 1))


def to_array(fp):
    fp.seek(0)
    return np.asarray(bytearray(fp.read()), dtype=np.uint8)


def cv2_decode(arr):
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def cv2_to_pygame(img):
    return pygame.image.frombuffer(img.tostring(), img.shape[1::-1], 'RGB')


class Kinect(object):
    def __init__(self):
        self.runtime = None
        self.double_buffer = DoubleBuffer(False, ['video', 'skeleton'])

    def video_frame_ready(self, frame):
        video, positions = process_frame(frame, VIDEO_RESOLUTION)
        self.double_buffer['video'] = video
        self.double_buffer['skeleton'] = positions

    def get_data(self):
        return self.double_buffer.get_all()

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
