import os

import xbmcgui
from control_item_group import ControlItemGroup
from lib import addon
from lib.gui.items.media_list_item import MediaListItem
from lib.utils.logger import Logger
from lib.utils.override import override


class MediaControlGroup(ControlItemGroup):
    __logger = Logger.get_instance(__name__)
    __WHITE_IMG_PATH = os.path.join(addon.ADDON_PATH, "resources", "media", "white.bmp")

    def __init__(self, width, height):
        border = xbmcgui.ControlImage(0, 0, 236, height, MediaControlGroup.__WHITE_IMG_PATH, 0, "00FFFFFF")
        poster = xbmcgui.ControlImage(5, 5, 236 - 10, height - 10, "", 0, "00FFFFFF")
        ControlItemGroup.__init__(self, width, height, [border, poster])
        return

    @override
    def _on_new_render(self, new_item):
        # type: (MediaListItem) -> None
        if new_item is not None:
            self._controls[1].setImage(new_item.getArt("poster"))
            self._controls[1].setColorDiffuse("FFFFFFFF")
        return

    @override
    def _on_focus(self):
        self._controls[0].setColorDiffuse("FFCBE354")
        return

    @override
    def _on_unfocus(self):
        self._controls[0].setColorDiffuse("00FFFFFF")
        return
