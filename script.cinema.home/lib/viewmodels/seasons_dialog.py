import xbmcgui
from lib import addon
from lib.models.json.show_info import ShowNfo
from lib.utils.logger import Logger
from lib.utils.override import override
from lib.viewmodels.episodes_dialog import EpisodesDialog

from lib.viewmodels.torrents_dialog import TorrentsDialog
from window import Window


class SeasonsDialog(xbmcgui.WindowXMLDialog, Window):
    __logger = Logger.get_instance(__name__)

    XML_ID_LIST = 190

    @classmethod
    def get_instance(cls, show_w_torrents):
        return SeasonsDialog('script-seasons_dialog.xml', addon.ADDON_PATH, 'default', '1080i',
                             show=show_w_torrents)

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self, args[0], args[1], args[2], args[3])
        Window.__init__(self)
        self.__show = kwargs['show']  # type: ShowNfo
        self.__seasons = self.__show.get_seasons()
        return

    def onInit(self):
        lst = self.getControlList(SeasonsDialog.XML_ID_LIST)
        if lst.size() == 0:
            self._render()
        return

    def _render(self):
        if self.__seasons is None or len(self.__seasons) == 0:
            return
        lst = self.getControlList(SeasonsDialog.XML_ID_LIST)
        items = [season.to_list_item() for season in self.__seasons]
        items.append(self._create_search_item())
        lst.addItems(items)
        self.setFocusId(SeasonsDialog.XML_ID_LIST)
        return

    @override
    def onAction(self, action):
        Window.onAction(self, action)
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            self.close()
        if action.getId() == xbmcgui.ACTION_SELECT_ITEM and self.getFocusId() == SeasonsDialog.XML_ID_LIST:
            lst = self.getControlList(SeasonsDialog.XML_ID_LIST)
            index = lst.getSelectedPosition()
            self.setProperty("Selected", str(True))
            if index < lst.size() - 1:
                self._on_click_season(index)
            else:
                self._on_click_search()
            self.clearProperty("Selected")
        return

    def _on_click_season(self, index):
        season = self.__seasons[index]
        if season.is_available() is False:
            xbmcgui.Dialog().ok(addon.ADDON.getLocalizedString(30005), addon.ADDON.getLocalizedString(30008))
            return
        dialog = EpisodesDialog.get_instance(season)
        dialog.doModal()
        del dialog
        return

    def _on_click_search(self):
        dialog = TorrentsDialog.get_instance(self.__show.get_all_torrents())
        dialog.doModal()
        del dialog
        return

    @staticmethod
    def _create_search_item():
        item = xbmcgui.ListItem()
        item.setInfo("video", {"title": "[I]{}...[/I]".format(addon.ADDON.getLocalizedString(30009))})
        item.setArt({'poster': "search_poster.png"})
        item.setInfo("video", {"plot": "...{}".format(addon.ADDON.getLocalizedString(30010))})
        return item
