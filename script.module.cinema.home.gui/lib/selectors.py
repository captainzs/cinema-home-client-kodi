from abc import ABCMeta, abstractmethod

from definitions import Alignment, Position


class Selector:
    __metaclass__ = ABCMeta

    @abstractmethod
    def next_up(self, alignment, from_position):
        # type: (Alignment, Position) -> Position
        pass

    @abstractmethod
    def next_down(self, alignment, from_position):
        # type: (Alignment, Position) -> Position
        pass

    @abstractmethod
    def next_left(self, alignment, from_position):
        # type: (Alignment, Position) -> Position
        pass

    @abstractmethod
    def next_right(self, alignment, from_position):
        # type: (Alignment, Position) -> Position
        pass

    @staticmethod
    def is_on_top(position):
        # type: (Position) -> bool
        return position.row == 0

    @staticmethod
    def is_on_bottom(alignment, position):
        # type: (Alignment, Position) -> bool
        return position.row == alignment.scope.rows - 1

    @staticmethod
    def is_on_left(position):
        # type: (Position) -> bool
        return position.column == 0

    @staticmethod
    def is_on_right(alignment, position):
        # type: (Alignment, Position) -> bool
        return position.column == alignment.scope.columns - 1


class StopSelector(Selector):
    def next_up(self, alignment, from_position):
        is_on_edge = Selector.is_on_top(from_position)
        return Position(from_position.column, from_position.row - 1) if not is_on_edge else from_position

    def next_down(self, alignment, from_position):
        is_on_edge = Selector.is_on_bottom(alignment, from_position)
        return Position(from_position.column, from_position.row + 1) if not is_on_edge else from_position

    def next_left(self, alignment, from_position):
        is_on_edge = Selector.is_on_left(from_position)
        return Position(from_position.column - 1, from_position.row) if not is_on_edge else from_position

    def next_right(self, alignment, from_position):
        is_on_edge = Selector.is_on_right(alignment, from_position)
        return Position(from_position.column + 1, from_position.row) if not is_on_edge else from_position
