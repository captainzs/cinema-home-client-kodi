import math

from control_list import ControlList
from definitions import Orientation, Vector, Position, Alignment, Scope
from lib.utils.logger import Logger
from lib.utils.override import override


class ControlPanel(ControlList):
    __logger = Logger.get_instance(__name__)

    def __init__(self, x, y, width, height, orientation=Orientation.HORIZONTAL,
                 scroller=None, scroll_stop=None, scroll_time=200,
                 layout=None, padding_left=0, padding_top=0, selector=None):
        ControlList.__init__(self, x, y, width, height, orientation, scroller, scroll_stop, scroll_time, layout,
                             padding_left, padding_top)
        self.__selector = selector
        return

    @staticmethod
    def _init_controls(width, height, orientation, layout):
        controls = []
        if layout is not None:
            has_space_for_horizontal = int(math.ceil(float(width) / layout.width()))
            has_space_for_vertical = int(math.ceil(float(height) / layout.height()))
            has_space_for = has_space_for_horizontal * has_space_for_vertical
            if orientation == Orientation.VERTICAL:
                can_animate_concurrently = has_space_for + 2 * has_space_for_horizontal
            else:
                can_animate_concurrently = has_space_for + 2 * has_space_for_vertical
            needed_for_animations = can_animate_concurrently * 2
            for i in range(0, needed_for_animations):
                controls.append(layout.new())
        return controls

    def alignment(self):
        size = self.size()
        if self.get_orientation() == Orientation.VERTICAL:
            max_columns = int(math.floor(float(self.getWidth()) / self._layout.width()))
            columns = min(size, max_columns)
            rows = int(math.ceil(float(size) / columns))
        else:
            max_rows = int(math.floor(float(self.getHeight()) / self._layout.height()))
            rows = min(size, max_rows)
            columns = int(math.ceil(float(size) / rows))
        return Alignment(size, Scope(columns, rows))

    @override
    def _item_position(self, item_index):
        position = self.__index_2_position(item_index)
        scroll_position = self.get_scroll_position()
        return Vector(self.getX() - scroll_position.x + self._padding_left + (self._layout.width() * position.column),
                      self.getY() - scroll_position.y + self._padding_top + (self._layout.height() * position.row))

    @override
    def move_up(self):
        new_position = self.__selector.next_up(self.alignment(), self.__index_2_position(self.getSelectedPosition()))
        return self.__move_to(new_position)

    @override
    def move_down(self):
        new_position = self.__selector.next_down(self.alignment(), self.__index_2_position(self.getSelectedPosition()))
        return self.__move_to(new_position)

    @override
    def move_left(self):
        new_position = self.__selector.next_left(self.alignment(), self.__index_2_position(self.getSelectedPosition()))
        return self.__move_to(new_position)

    @override
    def move_right(self):
        new_position = self.__selector.next_right(self.alignment(), self.__index_2_position(self.getSelectedPosition()))
        return self.__move_to(new_position)

    def __move_to(self, new_position):
        new_index = self.__position_2_index(new_position)
        if new_index == self.getSelectedPosition():
            return False
        return self.selectItem(new_index)

    def __index_2_position(self, index):
        if self.get_orientation() == Orientation.VERTICAL:
            max_columns = int(math.floor(float(self.getWidth()) / self._layout.width()))
            column_index = index % max_columns
            row_index = index / max_columns
        else:
            max_rows = int(math.floor(float(self.getHeight()) / self._layout.height()))
            column_index = index / max_rows
            row_index = index % max_rows
        return Position(column_index, row_index)

    def __position_2_index(self, position):
        alignment = self.alignment()
        if position.column >= alignment.scope.columns:
            return None
        if position.row >= alignment.scope.rows:
            return None
        if self.get_orientation() == Orientation.VERTICAL:
            index = position.row * alignment.scope.columns + position.column
        else:
            index = position.column * alignment.scope.rows + position.row
        return index
