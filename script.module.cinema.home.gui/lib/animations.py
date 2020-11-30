from abc import abstractmethod, ABCMeta

from lib.utils.override import override


class ListItemAnimation:
    __metaclass__ = ABCMeta

    @abstractmethod
    def to_list(self):
        pass

    @abstractmethod
    def persist(self, to_control):
        pass


class SlideAnimation(ListItemAnimation):
    def __init__(self, delta_x, delta_y):
        self.__delta_x = delta_x
        self.__delta_y = delta_y
        return

    @override
    def persist(self, to_control):
        to_control.setPosition(to_control.getX() + self.__delta_x, to_control.getY() + self.__delta_y)
        return

    @override
    def to_list(self, duration, condition):
        return [self.to_tuple(self.__delta_x, self.__delta_y, duration, condition)]

    @staticmethod
    def to_tuple(delta_x, delta_y, duration, condition):
        return ("conditional", 'effect=slide start=0,0 end={},{} time={} condition={} reversible=false'
                .format(delta_x, delta_y, duration, condition),)


class FadeAnimation(ListItemAnimation):
    def __init__(self, from_opacity, to_opacity):
        self.__from_opacity = from_opacity
        self.__to_opacity = to_opacity
        return

    @override
    def persist(self, to_control):
        to_control.set_opacity(self.__to_opacity)
        return

    @override
    def to_list(self, duration, condition):
        return [self.to_tuple(self.__from_opacity, self.__to_opacity, duration, condition),
                self.to_tuple(self.__from_opacity, self.__from_opacity, 0, "!{}".format(condition))]

    @staticmethod
    def to_tuple(from_opacity, to_opacity, duration=0, condition="true"):
        return ("conditional", 'effect=fade start={} end={} time={} condition={} reversible=false'
                .format(from_opacity, to_opacity, duration, condition),)


def has_effect(effect, animations):
    # type: (str, list[tuple[str,str]]) -> bool
    for animation in animations:
        attributes = animation[1]
        if "effect={}".format(effect) in attributes:
            return True
    return False


def find_all(by_effect, from_animations):
    filtered = []
    for animation in from_animations:
        attributes = animation[1]
        if "effect={}".format(by_effect) in attributes:
            filtered.append(animation)
    return filtered
