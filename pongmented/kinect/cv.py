import cv2
import numpy as np
import pygame

from numpy import uint8
from contour_data import ContourData


APPROX_POLY_DP_EPSILON = 0.001

MIN_THRESH = 240
MAX_BRIGHTNESS = 255
MAX_CHAIN_DISTANCE = 30
AREA_THRESHOLD = 1
ONES_KERNEL = np.ones((3, 3), np.uint8)


def reduce_noise(img):
    t = cv2.erode(img, ONES_KERNEL, iterations=1)
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


def distance(a, b):
    return np.linalg.norm(a - b)


def min_contour_distance(contour_data_a, contour_data_b):
    return distance(contour_data_a.center, contour_data_b.center)
    min_dist = None

    for ap in contour_data_a.poly:
        for bp in contour_data_b.poly:
            candidate = distance(ap, bp)
            if min_dist is None or candidate < min_dist:
                min_dist = candidate

    return min_dist


def find_chains(contour_data, all_contours_data, chain=None):
    chain = chain or set()
    chain.add(contour_data)

    for other_contour_data in all_contours_data:
        contour_distance = min_contour_distance(contour_data, other_contour_data)
        if other_contour_data not in chain and contour_distance <= MAX_CHAIN_DISTANCE:
            chain.update(find_chains(other_contour_data, all_contours_data, chain))

    return chain


def find_all_chains(contours_data):
    chains = set()
    contours_in_chains = set()

    for data in contours_data:
        if data not in contours_in_chains:
            chain = frozenset(find_chains(data, contours_data))
            chains.add(chain)
            contours_in_chains.update(chain)

    return chains


def thresh_channels(img):
    r, g, b = cv2.split(img)
    _, r = cv2.threshold(r, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)
    _, g = cv2.threshold(g, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)
    _, b = cv2.threshold(b, MIN_THRESH, MAX_BRIGHTNESS, cv2.THRESH_BINARY)
    return b, g, r


def get_chain_center(chain):
    chain_center = np.array([0.0, 0.0])
    areas = []

    for contour_data in chain:
        area = contour_data.area
        chain_center += contour_data.center.dot(area)
        areas.append(area)

    chain_center /= sum(areas)
    chain_center = np.array(np.rint(chain_center), dtype=np.int)
    return chain_center


def find_contours(threshed_channel, img):
    _, contours, _ = cv2.findContours(threshed_channel, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    contours_data = []

    for contour in contours:
        convex = cv2.convexHull(contour, returnPoints=False)
        poly = cv2.approxPolyDP(contour, APPROX_POLY_DP_EPSILON, closed=True)
        area = cv2.contourArea(poly)

        if area >= AREA_THRESHOLD:
            draw_convex(contour, convex, img)
            contour_center = np.array(get_contour_center(contour))
            contours_data.append(ContourData(contour_center, area, poly))

    return contours_data


def detect_players(img):
    t = thresh_green(img)
    t = reduce_noise(t)

    img = cv2.merge((t, t, t))

    contours_data = find_contours(t, img)
    chains = find_all_chains(contours_data)
    avg_positions = [get_chain_center(chain) for chain in chains]

    return cv2_to_pygame(img), np.array(avg_positions)


def thresh_white(img):
    b, g, r = thresh_channels(img)
    g = cv2.bitwise_and(cv2.bitwise_and(r, b), g)
    return g


def thresh_green(img):
    b, g, r = thresh_channels(img)
    g = cv2.bitwise_or(cv2.bitwise_and(cv2.bitwise_not(cv2.bitwise_or(r, b)), g), cv2.bitwise_and(cv2.bitwise_and(r, b), g))
    # g = cv2.bitwise_or(cv2.bitwise_not(cv2.bitwise_or(r, b)), g)

    return g


def thresh_red(img):
    b, g, r = thresh_channels(img)
    g = cv2.bitwise_and(cv2.bitwise_not(cv2.bitwise_or(b, g)), r)
    return g


def detect_from_bmp(bmp_fp):
    return detect_players(cv2.flip(cv2_decode(to_array(bmp_fp)), 1))
