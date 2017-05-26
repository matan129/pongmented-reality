import hashlib

import numpy as np


def hash_numpy_array(arr):
    return int(hashlib.sha1(arr.view(np.uint8)).hexdigest(), 16)


class ContourData(object):
    def __init__(self, center, area, poly):
        self.center = center
        self.area = area
        self.poly = poly

        self.__hash = hash((hash_numpy_array(center), area, hash_numpy_array(poly)))

    def __hash__(self):
        return self.__hash
