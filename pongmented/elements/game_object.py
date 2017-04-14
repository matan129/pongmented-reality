class GameObject(object):
    def __init__(self, window, space, event_manager):
        self.window = window
        self.w, self.h = self.window.get_size()
        self.space = space
        self.event_manager = event_manager
        self.state = {}

    def update(self):
        pass

    def render(self):
        raise NotImplementedError()
