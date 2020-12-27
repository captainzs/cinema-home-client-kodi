import xbmcgui
from control_list import ControlList
from definitions import Orientation
from item_layout import ItemLayout
from lib import addon
from lib.gui.media_set_control_group import MediaSetControlGroup
from lib.utils.logger import Logger
from lib.viewmodels.loading_dialog import LoadingDialog
from lib.viewmodels.more_window import MoreWindow
from scrollers import AlwaysScroller
from window import Window


class MainDialog(xbmcgui.WindowXMLDialog, Window):
    __logger = Logger.get_instance(__name__)

    XML_BTN_MORE = 99
    XML_PROP_SELECTED_MENU = "SelectedMenu"

    @classmethod
    def get_instance(cls):
        return MainDialog('script-main_dialog.xml', addon.ADDON_PATH, 'default', '1080i',
                          loading_dialog=LoadingDialog.get_instance())

    def __init__(self, *args, **kwargs):
        Window.__init__(self)
        self.__list = self.__init_controls()
        xbmcgui.WindowXMLDialog.__init__(self, args[0], args[1], args[2], args[3])
        self.__parent_window = None
        return

    def __init_controls(self):
        media_set_list = ControlList(0, 535, 1920, 545, orientation=Orientation.VERTICAL,
                                     scroller=AlwaysScroller(), scroll_time=300,
                                     layout=ItemLayout(width=1920, height=418, clazz=MediaSetControlGroup))
        self.addControl(media_set_list)
        return media_set_list

    def doModalOver(self, parent_window):
        self.__parent_window = parent_window
        self.doModal()
        return

    def onInit(self):
        self.__list.controlRight(self.getControl(MainDialog.XML_BTN_MORE))
        return

    def onAction(self, action):
        Window.onAction(self, action)
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            self.__parent_window.close()
        elif action.getId() == xbmcgui.ACTION_MOVE_LEFT and self.getFocusId() == MainDialog.XML_BTN_MORE:
            self.setFocus(self.__list)
        elif action.getId() in [xbmcgui.ACTION_MOVE_UP,
                                xbmcgui.ACTION_MOVE_DOWN] and self.getFocusId() == MainDialog.XML_BTN_MORE:
            self.setFocus(self.__list)
            self.__list.on_action(action)
        elif action.getId() == xbmcgui.ACTION_SELECT_ITEM:
            self.__on_select(self.getFocusId())

        if action.getId() in [xbmcgui.ACTION_MOVE_UP, xbmcgui.ACTION_MOVE_DOWN, xbmcgui.ACTION_MOVE_LEFT,
                              xbmcgui.ACTION_MOVE_RIGHT]:
            self._on_media_hovered()
        return

    def onFocus(self, control_id):
        Window.onFocus(self, control_id)
        if control_id == MainDialog.XML_BTN_MORE:
            self.__parent_window.update(None)
        return

    def __on_select(self, control_id):
        if control_id == MainDialog.XML_BTN_MORE:
            self.__on_more()
        elif control_id == self.__list.getId():
            self.close()
        return

    def __on_more(self):
        media_set = self.__list.getSelectedItem().get_set()
        if media_set is not None:
            window = MoreWindow.get_instance(media_set, MoreWindow.ColumnNo.x11)
            self.close()
            window.doModal()
            self.doModal()
        return

    def _get_list(self):
        return self.__list

    def _on_media_hovered(self):
        item = self.__list.getSelectedItem()
        if item is None:
            return
        media_item = item.get_selected_item()
        if media_item is None:
            return
        self.__parent_window.update(media_item.get_media())
        return
