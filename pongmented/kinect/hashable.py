from hashlib import sha1

from numpy import all
from numpy.core.multiarray import array
import numpy as np


class Hashable(object):
    def __init__(self, wrapped):
        self.__wrapped = array(wrapped)
        self.__hash = int(sha1(wrapped.view(np.uint8)).hexdigest(), 16)

    def __eq__(self, other):
        return all(self.__wrapped == other.__wrapped)

    def __hash__(self):
        return self.__hash

    def unwrap(self):
        return array(self.__wrapped)
