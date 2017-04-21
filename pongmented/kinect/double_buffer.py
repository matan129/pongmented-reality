import threading
import functools32


def locked(f):
    @functools32.wraps(f)
    def _wrapper(self, *args, **kwargs):
        with self.lock:
            return f(self, *args, **kwargs)
    return _wrapper


class DoubleBuffer(object):
    def __init__(self, consistent, keys):
        self.consistent = consistent
        self.keys = keys
        self.visible = {}
        self.buffered = {}
        self.status = {}
        self.lock = threading.RLock()
        self.flush()

    @locked
    def flush(self):
        for key, buffered_value in self.buffered.iteritems():
            self.visible[key] = buffered_value

        for key in self.keys:
            self.status[key] = False
            self.buffered[key] = None

    @locked
    def __setitem__(self, key, value):
        if key not in self.keys:
            raise ValueError('Unknown key: ' + key)

        self.buffered[key] = value
        self.status[key] = True

        if not self.consistent or all(self.status.values()):
            self.flush()

    @locked
    def __getitem__(self, item):
        return self.visible[item]

    @locked
    def get_all(self):
        return self.visible.copy()
