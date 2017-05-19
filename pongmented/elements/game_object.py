class GameObject(object):
    """
    Base class for objects that are shown in the game window.
    Most, if not all, objects have physical properties which are modelled by pymunk.
    """
    def __init__(self, window, space, event_manager):
        """
        :param window: The pygame window to draw onto. 
        :param space: The pymunk space that provides physical information.
        :param event_manager: see `~EventManager`
        """
        self.window = window
        self.w, self.h = self.window.get_size()
        self.space = space
        self.event_manager = event_manager
        self.state = {}

    def update(self):
        """
        Updates object properties.
        Called after the game state was updated.
        see `~PongEngine.push_state` and `~PongEngine.update_all`
        """
        pass

    def render(self):
        """
        Draws the object on the window.
        """
        raise NotImplementedError()
