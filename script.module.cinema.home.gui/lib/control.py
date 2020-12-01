from abc import ABCMeta, abstractmethod

from lib.utils.logger import Logger
from rect import Rect


class Control:
    __logger = Logger.get_instance(__name__)
    __metaclass__ = ABCMeta

    def __init__(self, x, y, width, height):
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

        self.__control_up = None
        self.__control_down = None
        self.__control_left = None
        self.__control_right = None

        self.__id = 0
        self.__parent = None
        self.__visible = True
        self.__animations = []
        return

    def getId(self):
        return self.__id

    def getX(self):
        return self.__x

    def getY(self):
        return self.__y

    def getWidth(self):
        return self.__width

    def getHeight(self):
        return self.__height

    def setPosition(self, x, y):
        self.__x = x
        self.__y = y
        return

    def setAnimations(self, animations):
        self.__animations = animations
        return

    def setVisible(self, visible):
        self.__visible = visible
        return

    def isVisible(self):
        return self.__visible

    def setNavigation(self, up, down, left, right):
        self.__control_up = up
        self.__control_down = down
        self.__control_left = left
        self.__control_right = right
        return

    def controlUp(self, control):
        self.__control_up = control
        return

    def controlDown(self, control):
        self.__control_down = control
        return

    def controlLeft(self, control):
        self.__control_left = control
        return

    def controlRight(self, control):
        self.__control_right = control
        return

    def get_control_up(self):
        return self.__control_up

    def get_control_down(self):
        return self.__control_down

    def get_control_left(self):
        return self.__control_left

    def get_control_right(self):
        return self.__control_right

    def get_visibility(self):
        if self.__parent is None:
            return False
        if not isinstance(self.__parent, Control):
            return True
        parent_visibility = self.__parent.get_visibility()
        return parent_visibility and self.__visible

    def get_parent(self):
        return self.__parent

    def bounds(self):
        return Rect(self.__x, self.__y, self.__width, self.__height)

    def attach(self, assigned_id, parent):
        if self.__parent is not None:
            raise RuntimeError("Control '{}' is already rendered to a container!".format(self.getId()))
        self.__id = assigned_id
        self.__parent = parent
        return []

    def get_animations(self):
        return self.__animations

    @abstractmethod
    def on_action(self, action):
        pass

    @abstractmethod
    def focus(self):
        pass

    @abstractmethod
    def unfocus(self):
        pass

    def __str__(self):
        return "Control - id:{} parent:{} bounds:{} visible:{} animations:{}".format(self.__id, id(self.__parent),
                                                                                     self.bounds(), self.__visible,
                                                                                     len(self.__animations))
