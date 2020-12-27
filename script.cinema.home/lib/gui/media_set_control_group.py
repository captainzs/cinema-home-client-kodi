from control_item_group import ControlItemGroup
from control_list import ControlList
from definitions import Orientation, ScrollStop, Vector
from item_layout import ItemLayout
from lib.gui.items.media_set_list_item import MediaSetPageListItem
from lib.gui.media_control_group import MediaControlGroup
from lib.utils.logger import Logger
from lib.utils.override import override
from scrollers import AlwaysScroller
from xbmcgui import ControlLabel


class MediaSetControlGroup(ControlItemGroup):
    __logger = Logger.get_instance(__name__)

    def __init__(self, width, height):
        label = ControlLabel(111, 0, 700, 52, "", "font15_bold", "FFFFFFFF", alignment=4)
        media_set_list = ControlList(0, 62, width, 344, orientation=Orientation.HORIZONTAL,
                                     scroller=AlwaysScroller(), scroll_stop=ScrollStop.LAST, scroll_time=200,
                                     layout=ItemLayout(240, 344, MediaControlGroup), padding_left=106)
        ControlItemGroup.__init__(self, width, height, [label, media_set_list])
        return

    @override
    def on_action(self, action):
        if self._controls[1].on_action(action) is True:
            self.get_item().set_selected_position(self._controls[1].getSelectedPosition())
            self.get_item().setProperty("ListScrollPositionX", str(self._controls[1].get_scroll_position().x))
            self.get_item().setProperty("ListScrollPositionY", str(self._controls[1].get_scroll_position().y))
            return True
        return False

    @override
    def _on_new_render(self, new_item):
        # type: (MediaSetPageListItem) -> None
        self._controls[1].reset()
        self._controls[0].setLabel("")
        if new_item is not None:
            self._controls[0].setLabel(new_item.get_name())
            selected = new_item.get_selected_position()
            scroll_x_str = new_item.getProperty("ListScrollPositionX")
            scroll_y_str = new_item.getProperty("ListScrollPositionY")
            scroll_x = int(scroll_x_str) if len(scroll_x_str) > 0 else 0
            scroll_y = int(scroll_y_str) if len(scroll_y_str) > 0 else 0
            self._controls[1].init_state(selected, Vector(scroll_x, scroll_y))
            self._controls[1].addItems(new_item.get_items())
        return

    @override
    def _on_focus(self):
        self.get_item().set_selected_position(self._controls[1].getSelectedPosition())
        self._controls[1].focus()
        return

    @override
    def _on_unfocus(self):
        self._controls[1].unfocus()
        return
