from abc import ABCMeta, abstractmethod

from definitions import Vector


class Scroller:
    __metaclass__ = ABCMeta

    def __init__(self):
        return

    @abstractmethod
    def direction_vector(self, focus_from, focus_to):
        # type: (Vector,Vector) -> Vector
        pass


class AlwaysScroller(Scroller):
    def __init__(self):
        Scroller.__init__(self)
        return

    def direction_vector(self, focus_from, focus_to):
        return Vector(int(focus_to.x - focus_from.x), int(focus_to.y - focus_from.y))


class FixedCenterScroller(Scroller):
    def __init__(self, center):
        # type: (Vector) -> None
        Scroller.__init__(self)
        self.__center = center
        return

    def direction_vector(self, focus_from, focus_to):
        from_2_to_x = abs(focus_to.x - focus_from.x)
        from_2_mid_x = abs(self.__center.x - focus_from.x)
        if from_2_to_x <= from_2_mid_x:
            scroll_value_x = 0
        else:
            scroll_value_x = abs(self.__center.x - focus_to.x)
        scroll_vector_x = scroll_value_x if (focus_to.x >= focus_from.x) else -scroll_value_x

        from_2_to_y = abs(focus_to.y - focus_from.y)
        from_2_mid_y = abs(self.__center.y - focus_from.y)
        if from_2_to_y <= from_2_mid_y:
            scroll_value_y = 0
        else:
            scroll_value_y = abs(self.__center.y - focus_to.y)
        scroll_vector_y = scroll_value_y if (focus_to.y >= focus_from.y) else -scroll_value_y
        return Vector(int(scroll_vector_x), int(scroll_vector_y))
