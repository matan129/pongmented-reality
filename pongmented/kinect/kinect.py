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
RADIUS = 100
VIDEO_RESOLUTION = 640, 480
AREA_THRESHOLD = 180
ONES_KERNEL = np.ones((3, 3), np.uint8)


from hashlib import sha1

from numpy import all, array, uint8


class hashable(object):
    r'''Hashable wrapper for ndarray objects.

        Instances of ndarray are not hashable, meaning they cannot be added to
        sets, nor used as keys in dictionaries. This is by design - ndarray
        objects are mutable, and therefore cannot reliably implement the
        __hash__() method.

        The hashable class allows a way around this limitation. It implements
        the required methods for hashable objects in terms of an encapsulated
        ndarray object. This can be either a copied instance (which is safer)
        or the original object (which requires the user to be careful enough
        not to modify it).
    '''
    def __init__(self, wrapped, tight=False):
        r'''Creates a new hashable object encapsulating an ndarray.

            wrapped
                The wrapped ndarray.

            tight
                Optional. If True, a copy of the input ndaray is created.
                Defaults to False.
        '''
        self.__tight = tight
        self.__wrapped = array(wrapped) if tight else wrapped
        self.__hash = int(sha1(wrapped.view(uint8)).hexdigest(), 16)

    def __eq__(self, other):
        return all(self.__wrapped == other.__wrapped)

    def __hash__(self):
        return self.__hash

    def unwrap(self):
        r'''Returns the encapsulated ndarray.

            If the wrapper is "tight", a copy of the encapsulated ndarray is
            returned. Otherwise, the encapsulated ndarray itself is returned.
        '''
        if self.__tight:
            return array(self.__wrapped)

        return self.__wrapped


def reduce_noise(img):
    t = cv2.erode(img, ONES_KERNEL, iterations=1)
    return cv2.dilate(t, ONES_KERNEL, iterations=4)


def draw_contour(cnt, h, img):
    defects = cv2.convexityDefects(cnt, h)
    if defects is not None and defects.shape:
        for i in xrange(defects.shape[0]):
            s, e, f, d = defects[i, 0]
            start = tuple(cnt[s][0])
            end = tuple(cnt[e][0])
            cv2.line(img, start, end, [0, MAX_BRIGHTNESS, 0], 2)


def get_contour_center(cnt):
    avg = np.mean(cnt, axis=1)
    x = int(round(avg[0, 0]))
    y = int(round(avg[0, 1]))
    return x, y


def to_array(fp):
    fp.seek(0)
    return np.asarray(bytearray(fp.read()), dtype=np.uint8)


def cv2_decode(arr):
    return cv2.imdecode(arr, cv2.IMREAD_COLOR)


def cv2_to_pygame(img):
    return pygame.image.frombuffer(img.tostring(), img.shape[1::-1], 'RGB')


def find_chains(contour_center, centers, chain=None):
    chain = chain or set()
    chain.add(contour_center)
    for other_center in centers:
        if other_center not in chain and np.linalg.norm(contour_center.unwrap() - other_center.unwrap()) <= RADIUS:
            chain.update(find_chains(other_center, centers, chain))

    return chain


class Kinect(object):
    def __init__(self):
        self.runtime = None
        self.double_buffer = DoubleBuffer(False, ['video', 'skeleton'])

    def video_frame_ready(self, frame):
        video, positions = self.process_frame(frame, VIDEO_RESOLUTION)
        self.double_buffer['video'] = video
        self.double_buffer['skeleton'] = positions

    def detect(self, img):
        b, g, r = self.thresh_channels(img)

        bright_channels = cv2.bitwise_or(r, b)
        g = cv2.bitwise_and(bright_channels, g)
        g = reduce_noise(g)
        _, contours, _ = cv2.findContours(g, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        img = cv2.merge((g, g, g))

        centers_to_areas = {}
        for cnt in contours:
            h = cv2.convexHull(cnt, returnPoints=False)
            area = cv2.contourArea(cv2.approxPolyDP(cnt, 0.001, True))

            if area >= AREA_THRESHOLD:
                draw_contour(cnt, h, img)
                contour_center = hashable(np.array(get_contour_center(cnt)))
                centers_to_areas[contour_center] = area

        chains = set()
        for contour_center, contour_area in centers_to_areas.iteritems():
            chains.add(frozenset(find_chains(contour_center, centers_to_areas.keys())))

        avg_positions = []
        for chain in chains:
            chain_center = np.array([0.0, 0.0])
            areas = []
            for center in chain:
                area = centers_to_areas[center]
                chain_center += center.unwrap().dot(area)
                areas.append(area)

            chain_center /= sum(areas)
            chain_center = np.array(np.rint(chain_center), dtype=np.int)
            avg_positions.append(chain_center)

        return cv2_to_pygame(img), avg_positions

    def thresh_channels(self, img):
        r, g, b = cv2.split(img)
        _, r = cv2.threshold(r, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY_INV)
        _, g = cv2.threshold(g, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)
        _, b = cv2.threshold(b, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY_INV)
        return b, g, r

    def process_frame(self, frame, resolution):
        image = Image.frombytes('RGBA', resolution, buffer(frame.image.bits), 'raw', 'BGRA')
        fp = io.BytesIO()
        image.save(fp, 'bmp')
        return self.detect(cv2.flip(cv2_decode(to_array(fp)), 1))

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
