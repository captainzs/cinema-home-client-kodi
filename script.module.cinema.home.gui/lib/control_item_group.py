from abc import abstractmethod, ABCMeta

from control_group import ControlGroup
from lib.utils.logger import Logger
from lib.utils.override import override
from xbmcgui import ListItem


class ControlItemGroup(ControlGroup):
    __logger = Logger.get_instance(__name__)
    __metaclass__ = ABCMeta

    def __init__(self, width, height, controls=None):
        ControlGroup.__init__(self, 0, 0, width, height, controls)
        self.__item = None
        return

    def get_item(self):
        return self.__item

    def render(self, item):
        if self.__item != item:
            self._on_new_render(item)
            if item is None:
                self.setVisible(False)
            self.__item = item
        return

    @override
    def focus(self):
        self.__item.select(True)
        self._on_focus()
        return

    @override
    def unfocus(self):
        self.__item.select(False)
        self._on_unfocus()
        return

    @abstractmethod
    def _on_new_render(self, new_item):
        # type: (ListItem) -> None
        return

    @abstractmethod
    def _on_focus(self):
        # type: () -> None
        return

    @abstractmethod
    def _on_unfocus(self):
        # type: () -> None
        return
