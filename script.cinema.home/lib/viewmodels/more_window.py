import math
import threading
import time

import xbmcgui
from lib import addon
from lib.services.client_service import ClientService
from lib.utils.logger import Logger
from lib.utils.override import override
from lib.viewmodels.details_window import DetailsWindow
from window import Window


class MoreWindow(xbmcgui.WindowXML, Window):
    _logger = Logger.get_instance(__name__)

    class ColumnNo:
        def __init__(self):
            pass

        x13 = 13
        x11 = 11

    SCROLL_TIME_WAIT_SECS = 0.5
    PAGE_MAX = 30

    XML_ID_PANEL = 200
    XML_PROP_COLUMN_COUNT = "ColumnCount"
    XML_PROP_MEDIA_SET_NAME = "MediaSetName"
    XML_CONSTRAINT_BORDER = 1
    XML_CONSTRAINT_HEADER = 0

    @classmethod
    def get_instance(cls, media_set, column_no):
        return MoreWindow('script-more_{}_window.xml'.format(column_no), addon.ADDON_PATH, 'default', '1080i', True,
                          column_no=column_no,
                          service=ClientService.get_instance(),
                          media_set=media_set)

    def __init__(self, *args, **kwargs):
        Window.__init__(self)
        xbmcgui.WindowXML.__init__(self, args[0], args[1], args[2], args[3], args[4])
        self.__column_no = kwargs["column_no"]
        self.__service = kwargs['service']
        self.__mset = kwargs['media_set']

        self.__rows_count_exact = MoreWindow.__init_calculations(self.__column_no)
        self.__current_screen_row = 0
        self.__updater_thread = None
        self.__focus_thief = xbmcgui.ControlButton(-50, -50, 0, 0, "")
        self.addControl(self.__focus_thief)
        return

    @staticmethod
    def __init_calculations(column_no):
        width = xbmcgui.getScreenWidth()
        height = xbmcgui.getScreenHeight() - MoreWindow.XML_CONSTRAINT_HEADER
        item_layout_width = int(math.floor(float(width) / column_no))
        i_width = item_layout_width - 2 * MoreWindow.XML_CONSTRAINT_BORDER
        i_height = int(round(i_width * 1.4725))
        item_layout_height = i_height + 2 * MoreWindow.XML_CONSTRAINT_BORDER
        rows_count = float(height) / item_layout_height
        return rows_count

    @override
    def onInit(self):
        self.setProperty(MoreWindow.XML_PROP_MEDIA_SET_NAME, self.__mset.get_name())
        if self.__updater_thread is None:
            self.__updater_thread = threading.Thread(target=self.__updater_task, args=())
            self.__updater_thread.start()
        return

    @override
    def onAction(self, action):
        Window.onAction(self, action)
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            self.close()
        elif action.getId() in [xbmcgui.ACTION_MOVE_LEFT, xbmcgui.ACTION_MOVE_RIGHT, xbmcgui.ACTION_MOVE_UP,
                                xbmcgui.ACTION_MOVE_DOWN]:
            if action.getId() == xbmcgui.ACTION_MOVE_DOWN:
                if self.__current_screen_row != math.floor(self.__rows_count_exact) - 1:
                    self.__current_screen_row += 1
            elif action.getId() == xbmcgui.ACTION_MOVE_UP:
                if self.__current_screen_row != 0:
                    self.__current_screen_row -= 1
        elif action.getId() == xbmcgui.ACTION_SELECT_ITEM:
            self.__on_select()
        return

    def __on_select(self):
        item = self.getControlList(MoreWindow.XML_ID_PANEL).getSelectedItem()
        if item is None:
            return
        media = self.__mset.get_media(item.getUniqueID("imdb"))
        details_window = DetailsWindow.get_instance()
        details_window.doModalWith(media)
        return

    def __updater_task(self):
        panel = self.getControlList(MoreWindow.XML_ID_PANEL)
        max_rows = math.ceil(self.__rows_count_exact)

        next_page_no = 1
        next_items = self.__load_page_items(next_page_no)
        next_page_needed = False
        while self.is_opened() and next_page_no <= MoreWindow.PAGE_MAX:
            if next_page_needed is False:
                next_page_needed = panel.size() - (panel.getSelectedPosition() + 1) <= max_rows * self.__column_no
            if next_items is None:
                next_items = self.__load_page_items(next_page_no)
                if next_items is None:
                    break
            focus_on_end = (panel.size() <= max_rows * self.__column_no) or (
                    self.__current_screen_row == math.floor(self.__rows_count_exact) - 1)
            if next_page_needed is True and focus_on_end is True:
                self.setFocusId(self.__focus_thief)
                time.sleep(MoreWindow.SCROLL_TIME_WAIT_SECS)
                position_before_insert = max(0, panel.getSelectedPosition())
                panel.addItems(next_items)
                next_items = None
                next_page_no += 1
                next_page_needed = False
                panel.selectItem(position_before_insert)
                self.setFocus(panel)
            else:
                time.sleep(0.1)
        return

    def __load_page_items(self, page_no):
        if page_no is None:
            return None
        page = self.__mset.page(page_no)
        if page is None:
            unfiltered_new_page = self.__service.request_lst(self.__mset.get_path(page_no), self.__mset.get_body(),
                                                             self.__mset.get_media_type())
            page = self.__mset.extend(page_no, unfiltered_new_page)
        return [media.to_list_item() for media in page]
