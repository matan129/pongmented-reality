from cv2 import cv2
import numpy as np
import pygame

from numpy import uint8
from hashable import Hashable

MIN_THRESH = 230
MAX_BRIGHTNESS = 255
CHAIN_RADIUS = 100
AREA_THRESHOLD = 50
ONES_KERNEL = np.ones((3, 3), np.uint8)


def reduce_noise(img):
    t = cv2.erode(img, ONES_KERNEL, iterations=2)
    return cv2.dilate(t, ONES_KERNEL, iterations=4)


def draw_convex(contour, h, img):
    defects = cv2.convexityDefects(contour, h)

    if defects is None or not defects.shape:
        return

    for i in xrange(defects.shape[0]):
        s, e, f, d = defects[i, 0]
        start = tuple(contour[s][0])
        end = tuple(contour[e][0])
        cv2.line(img, start, end, [0, 255, 0], 2)


def get_contour_center(contour):
    m = cv2.moments(contour)
    cx = int(m['m10'] / m['m00'])
    cy = int(m['m01'] / m['m00'])
    return cx, cy


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
        if other_center not in chain and distance(contour_center.unwrap(), other_center.unwrap()) <= CHAIN_RADIUS:
            chain.update(find_chains(other_center, centers, chain))

    return chain


def distance(contour_center, other_center):
    return np.linalg.norm(contour_center - other_center)


def thresh_channels(img):
    r, g, b = cv2.split(img)
    _, r = cv2.threshold(r, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)
    _, g = cv2.threshold(g, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)
    _, b = cv2.threshold(b, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)
    return b, g, r


def average_chain(centers_to_areas, chain):
    chain_center = np.array([0.0, 0.0])
    areas = []
    for center in chain:
        area = centers_to_areas[center]
        chain_center += center.unwrap().dot(area)
        areas.append(area)
    chain_center /= sum(areas)
    chain_center = np.array(np.rint(chain_center), dtype=np.int)
    return chain_center


def find_all_chains(centers_to_areas):
    chains = set()
    for contour_center, contour_area in centers_to_areas.iteritems():
        chains.add(frozenset(find_chains(contour_center, centers_to_areas.keys())))
    return chains


def find_contours(threshed_channel, img):
    _, contours, _ = cv2.findContours(threshed_channel, cv2.RETR_LIST, cv2.CHAIN_APPROX_TC89_KCOS)
    centers_to_areas = {}
    for contour in contours:
        convex = cv2.convexHull(contour, returnPoints=False)
        area = cv2.contourArea(cv2.approxPolyDP(contour, 1, True))

        if area >= AREA_THRESHOLD:
            draw_convex(contour, convex, img)
            contour_center_arr = np.array(get_contour_center(contour))
            contour_center_arr.flags.writeable = False
            contour_center = Hashable(contour_center_arr)
            centers_to_areas[contour_center] = area
    return centers_to_areas


def detect_players(img):
    g = thresh_white(img)
    g = reduce_noise(g)

    img = cv2.merge((g, g, g))
    centers_to_areas = find_contours(g, img)

    chains = find_all_chains(centers_to_areas)
    avg_positions = [average_chain(centers_to_areas, chain) for chain in chains]

    return cv2_to_pygame(img), np.array(avg_positions)


def thresh_white(img):
    b, g, r = thresh_channels(img)
    g = cv2.bitwise_and(cv2.bitwise_and(r, b), g)
    return g


def thresh_green(img):
    b, g, r = thresh_channels(img)
    g = cv2.bitwise_and(cv2.bitwise_not(cv2.bitwise_or(r, b)), g)
    return g


def thresh_red(img):
    b, g, r = thresh_channels(img)
    g = cv2.bitwise_and(cv2.bitwise_not(cv2.bitwise_or(b, g)), r)
    return g


def detect_from_bmp(bmp_fp):
    return detect_players(cv2.flip(cv2_decode(to_array(bmp_fp)), 1))
