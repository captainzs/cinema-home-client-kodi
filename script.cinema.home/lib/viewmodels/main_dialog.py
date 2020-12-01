import threading
import time

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

    XML_ID_MENU_SEARCH = 34
    XML_ID_MENU_MOVIES = 35
    XML_ID_MENU_SHOWS = 36
    XML_ID_MENU_FAVORITES = 37
    XML_BTN_MORE = 99

    XML_PROP_SELECTED_MENU = "SelectedMenu"
    XML_PROP_LST_FOCUSED = "IsListFocused"

    @classmethod
    def get_instance(cls):
        return MainDialog('script-main_dialog.xml', addon.ADDON_PATH, 'default', '1080i',
                          loading_dialog=LoadingDialog.get_instance())

    def __init__(self, *args, **kwargs):
        Window.__init__(self)
        self.__list = self.__init_controls()
        xbmcgui.WindowXMLDialog.__init__(self, args[0], args[1], args[2], args[3])

        self.__loading_dialog = kwargs['loading_dialog']

        self.__movie_groups = None
        self.__show_groups = None
        self.__start_menu = None
        self.__parent_window = None
        return

    def __init_controls(self):
        media_set_list = ControlList(0, 535, 1920, 545, orientation=Orientation.VERTICAL,
                                     scroller=AlwaysScroller(), scroll_time=300,
                                     layout=ItemLayout(width=1920, height=418, clazz=MediaSetControlGroup))
        self.addControl(media_set_list)
        return media_set_list

    def set_up(self, movie_groups, show_groups, start_menu):
        if self.is_opened():
            return
        self.__movie_groups = movie_groups
        self.__show_groups = show_groups
        self.__start_menu = start_menu
        return

    def doModalOver(self, parent_window):
        self.__parent_window = parent_window
        self.doModal()
        return

    def onInit(self):
        if self.__selected_menu_id() is None:
            self.__on_select(self.__start_menu)
            if self.__list.size() == 0:
                self.setFocusId(self.__start_menu)
        self.__list.controlRight(self.getControl(MainDialog.XML_BTN_MORE))
        return

    def onAction(self, action):
        Window.onAction(self, action)
        is_menu_focused = self.getFocusId() in [MainDialog.XML_ID_MENU_SEARCH, MainDialog.XML_ID_MENU_MOVIES,
                                                MainDialog.XML_ID_MENU_SHOWS, MainDialog.XML_ID_MENU_FAVORITES]
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            if self.getFocus() == self.__list:
                self.setFocusId(self.__selected_menu_id())
            else:
                self.__parent_window.close()
        elif action.getId() == xbmcgui.ACTION_MOVE_RIGHT and is_menu_focused is True and self.__list.size() > 0:
            self.setFocus(self.__list)
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
            self.__on_media_hovered()
            return

    def onFocus(self, control_id):
        Window.onFocus(self, control_id)
        if control_id == MainDialog.XML_BTN_MORE:
            self.__parent_window.update(None)
        elif control_id == self.__list.getId():
            self.setProperty(MainDialog.XML_PROP_LST_FOCUSED, str(True))
        elif control_id in [MainDialog.XML_ID_MENU_SEARCH, MainDialog.XML_ID_MENU_MOVIES,
                            MainDialog.XML_ID_MENU_SHOWS, MainDialog.XML_ID_MENU_FAVORITES]:
            self.clearProperty(MainDialog.XML_PROP_LST_FOCUSED)
        return

    def __on_select(self, control_id):
        if control_id == MainDialog.XML_ID_MENU_MOVIES:
            self.__on_movies()
        elif control_id == MainDialog.XML_ID_MENU_SHOWS:
            self.__on_shows()
        elif control_id == MainDialog.XML_BTN_MORE:
            self.__on_more()
        elif control_id == self.__list.getId():
            self.close()
        return

    def __on_movies(self):
        if self.__selected_menu_id() == MainDialog.XML_ID_MENU_MOVIES:
            self.setFocus(self.__list)
            return
        if self.is_opened() and self.__render(self.__movie_groups) is True:
            self.setProperty(MainDialog.XML_PROP_SELECTED_MENU, str(MainDialog.XML_ID_MENU_MOVIES))
            self.__on_unfocus_menu()
            self.__list.controlLeft(self.getControl(MainDialog.XML_ID_MENU_MOVIES))
        return

    def __on_shows(self):
        if self.__selected_menu_id() == MainDialog.XML_ID_MENU_SHOWS:
            self.setFocus(self.__list)
            return
        if self.is_opened() and self.__render(self.__show_groups) is True:
            self.setProperty(MainDialog.XML_PROP_SELECTED_MENU, str(MainDialog.XML_ID_MENU_SHOWS))
            self.__on_unfocus_menu()
            self.__list.controlLeft(self.getControl(MainDialog.XML_ID_MENU_SHOWS))
        return

    def __render(self, media_sets):
        if self.__list is None or media_sets is None:
            return False
        valid_media_set_items = self.__loading_dialog.load(20, self._wait_and_get_not_empty, media_sets)
        if valid_media_set_items is not None and len(valid_media_set_items) > 0:
            self.__list.reset()
            self.__list.addItems(valid_media_set_items)
            self.setFocus(self.__list)
            self.__on_media_hovered()
            return True
        return False

    def __selected_menu_id(self):
        id_str = self.getProperty(MainDialog.XML_PROP_SELECTED_MENU)
        return int(id_str) if id_str is not "" else None

    def __on_more(self):
        media_set = self.__list.getSelectedItem().get_set()
        if media_set is not None:
            window = MoreWindow.get_instance(media_set, MoreWindow.ColumnNo.x11)
            self.close()
            window.doModal()
            self.doModal()
        return

    def __on_media_hovered(self):
        item = self.__list.getSelectedItem()
        media_item = item.get_selected_item()
        self.__parent_window.update(media_item.get_media())
        return

    def __on_unfocus_menu(self):
        self.setProperty("SearchLabel", "")
        self.setProperty("MoviesLabel", "")
        self.setProperty("ShowsLabel", "")
        self.setProperty("FavoritesLabel", "")
        return

    @staticmethod
    def _wait_and_get_not_empty(media_sets):
        threads = []
        ready_lst = []
        items_lst = []
        while len(ready_lst) != len(media_sets):
            for media_set in media_sets:
                if media_set not in ready_lst:
                    page1 = media_set.page(1)
                    if page1 is not None:
                        ready_lst.append(media_set)
                        if len(page1) != 0:
                            t = threading.Thread(target=lambda s: items_lst.append(s.to_list_item()), args=(media_set,))
                            threads.append(t)
                            t.start()
            time.sleep(0.01)
        for t in threads:
            t.join()
        return sorted(items_lst, key=lambda si: media_sets.index(si.get_set()))
