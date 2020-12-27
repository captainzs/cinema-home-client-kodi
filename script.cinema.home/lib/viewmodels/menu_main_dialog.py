import threading

import xbmcgui
from lib import addon
from lib.models.types.media_sets import Search
from lib.services import mset_factory
from lib.utils.logger import Logger
from lib.viewmodels.loading_dialog import LoadingDialog
from lib.viewmodels.main_dialog import MainDialog


class MenuMainDialog(MainDialog):
    __logger = Logger.get_instance(__name__)

    PAGE_TO_LOAD = 1
    MENU_LOAD_TIMEOUT_SECS = 20

    XML_ID_MENU_SEARCH = 34
    XML_ID_MENU_MOVIES = 35
    XML_ID_MENU_SHOWS = 36
    XML_ID_MENU_FAVORITES = 37

    @classmethod
    def get_instance(cls):
        return MenuMainDialog('script-main_dialog.xml', addon.ADDON_PATH, 'default', '1080i',
                              loading_dialog=LoadingDialog.get_instance())

    def __init__(self, *args, **kwargs):
        MainDialog.__init__(self, *args, **kwargs)
        self.__loading_dialog = kwargs['loading_dialog']
        self.__movie_mset_items = None
        self.__show_mset_items = None
        return

    def onInit(self):
        MainDialog.onInit(self)
        if self.selected_menu_id() is None:
            self.open_movies_menu()
            self.__focus_lst()
        return

    def onAction(self, action):
        is_menu_focused = self.getFocusId() in [MenuMainDialog.XML_ID_MENU_SEARCH, MenuMainDialog.XML_ID_MENU_MOVIES,
                                                MenuMainDialog.XML_ID_MENU_SHOWS, MenuMainDialog.XML_ID_MENU_FAVORITES]
        if not is_menu_focused and (
                action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK):
            self.setFocusId(self.selected_menu_id())
        elif action.getId() == xbmcgui.ACTION_MOVE_RIGHT and is_menu_focused is True and self._get_list().size() > 0:
            self.__focus_lst()
        elif action.getId() == xbmcgui.ACTION_SELECT_ITEM and is_menu_focused:
            self.__focus_lst()
        else:
            MainDialog.onAction(self, action)
        return

    def onClick(self, control_id):
        MainDialog.onClick(self, control_id)
        if control_id == MenuMainDialog.XML_ID_MENU_SEARCH:
            self.open_search_menu()
        elif control_id == MenuMainDialog.XML_ID_MENU_MOVIES:
            self.open_movies_menu()
        elif control_id == MenuMainDialog.XML_ID_MENU_SHOWS:
            self.open_shows_menu()
        return

    def open_search_menu(self):
        if not self.is_opened():
            return
        query = xbmcgui.Dialog().input(addon.ADDON.getLocalizedString(30026))
        if query == "":
            return
        mset_items = self.__loading_dialog.load(MenuMainDialog.MENU_LOAD_TIMEOUT_SECS, self.load_search_menu, query)
        if mset_items is None or len(mset_items) == 0:
            return
        self.setProperty(MainDialog.XML_PROP_SELECTED_MENU, str(MenuMainDialog.XML_ID_MENU_SEARCH))
        self._get_list().controlLeft(self.getControl(MenuMainDialog.XML_ID_MENU_SEARCH))
        self.__render(mset_items)
        return

    def load_search_menu(self, query_str):
        media_sets = [Search.movies(query_str), Search.shows(query_str)]
        return self.__load_mset_items(media_sets)

    def open_movies_menu(self):
        if not self.is_opened() or self.selected_menu_id() == MenuMainDialog.XML_ID_MENU_MOVIES:
            return
        mset_items = self.__loading_dialog.load(MenuMainDialog.MENU_LOAD_TIMEOUT_SECS, self.load_movies_menu)
        if mset_items is None or len(mset_items) == 0:
            return
        self.setProperty(MainDialog.XML_PROP_SELECTED_MENU, str(MenuMainDialog.XML_ID_MENU_MOVIES))
        self._get_list().controlLeft(self.getControl(MenuMainDialog.XML_ID_MENU_MOVIES))
        self.__render(mset_items)
        return

    def load_movies_menu(self):
        if self.__movie_mset_items is None:
            self.__movie_mset_items = self.__load_mset_items(mset_factory.movie_sets())
        return self.__movie_mset_items

    def open_shows_menu(self):
        if not self.is_opened() or self.selected_menu_id() == MenuMainDialog.XML_ID_MENU_SHOWS:
            return
        mset_items = self.__loading_dialog.load(MenuMainDialog.MENU_LOAD_TIMEOUT_SECS, self.load_shows_menu)
        if mset_items is None or len(mset_items) == 0:
            return
        self.setProperty(MainDialog.XML_PROP_SELECTED_MENU, str(MenuMainDialog.XML_ID_MENU_SHOWS))
        self._get_list().controlLeft(self.getControl(MenuMainDialog.XML_ID_MENU_SHOWS))
        self.__render(mset_items)
        return

    def load_shows_menu(self):
        if self.__show_mset_items is None:
            self.__show_mset_items = self.__load_mset_items(mset_factory.show_sets())
        return self.__show_mset_items

    def __load_mset_items(self, media_sets):
        threads = []
        items_lst = []
        for mset in media_sets:
            t = threading.Thread(target=lambda s: items_lst.append(s.to_list_item(MenuMainDialog.PAGE_TO_LOAD)),
                                 args=(mset,))
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        non_empty_items = [i for i in items_lst if not i.is_empty()]
        return sorted(non_empty_items, key=lambda mset_item: media_sets.index(mset_item.get_set()))

    def __render(self, mset_items):
        self._get_list().reset()
        self._get_list().addItems(mset_items)
        self._on_media_hovered()
        return

    def __focus_lst(self):
        self.setFocus(self._get_list())
        self.__on_unfocus_menu()
        return

    def selected_menu_id(self):
        id_str = self.getProperty(MainDialog.XML_PROP_SELECTED_MENU)
        return int(id_str) if id_str is not "" else None

    def __on_unfocus_menu(self):
        self.setProperty("SearchLabel", "")
        self.setProperty("MoviesLabel", "")
        self.setProperty("ShowsLabel", "")
        self.setProperty("FavoritesLabel", "")
        return
