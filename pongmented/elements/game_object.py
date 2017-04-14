class GameObject(object):
    def __init__(self, window, space):
        self.window = window
        self.w, self.h = self.window.get_size()
        self.space = space
        self.state = {}

    def update(self):
        pass

    def render(self):
        raise NotImplementedError()
