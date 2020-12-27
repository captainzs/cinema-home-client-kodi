import xbmcgui
from lib import addon
from lib.models.json.season_info import Season
from lib.services.client_service import ClientService
from lib.utils.logger import Logger
from lib.utils.override import override
from lib.viewmodels.torrents_dialog import TorrentsDialog
from window import Window


class EpisodesDialog(xbmcgui.WindowXMLDialog, Window):
    _logger = Logger.get_instance(__name__)

    XML_ID_LIST_FAKE = 50
    XML_ID_BTN_SEASON = 51
    XML_ID_PANEL = 52

    @classmethod
    def get_instance(cls, season):
        return EpisodesDialog('script-episodes_dialog.xml', addon.ADDON_PATH, 'default', '1080i',
                              season=season,
                              client_service=ClientService.get_instance())

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self, args[0], args[1], args[2], args[3])
        Window.__init__(self)
        self.__season = kwargs['season']  # type: Season
        self.__episodes = self.__season.get_episodes()
        self.__service = kwargs['client_service']  # type: ClientService
        return

    def onInit(self):
        lst = self.getControlList(EpisodesDialog.XML_ID_PANEL)
        self.setProperty("FullSeasonDownloadable", str(self.__season.is_downloadable()))
        if lst.size() == 0:
            self._render()
        self.setProperty("EpisodesCount", str(lst.size()))
        return

    def _render(self):
        if self.__episodes is None or len(self.__episodes) == 0:
            self.__on_download_season()
            self.close()
            return
        lst = self.getControlList(EpisodesDialog.XML_ID_PANEL)
        lst.addItems([self.__panel_item(episode) for episode in self.__episodes])
        self.setFocusId(EpisodesDialog.XML_ID_PANEL)
        return

    @override
    def onAction(self, action):
        Window.onAction(self, action)
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            self.close()
        if self.getFocusId() == EpisodesDialog.XML_ID_PANEL:
            index = self.getControlList(EpisodesDialog.XML_ID_PANEL).getSelectedPosition()
            if action.getId() == xbmcgui.ACTION_SELECT_ITEM:
                self.__on_download(index)
            elif action.getId() in [xbmcgui.ACTION_MOVE_LEFT, xbmcgui.ACTION_MOVE_RIGHT, xbmcgui.ACTION_MOVE_UP,
                                    xbmcgui.ACTION_MOVE_DOWN]:
                self.__on_hover_episode(index)
            return

    @override
    def onFocus(self, control_id):
        Window.onFocus(self, control_id)
        if control_id == EpisodesDialog.XML_ID_PANEL:
            index = self.getControlList(EpisodesDialog.XML_ID_PANEL).getSelectedPosition()
            self.__on_hover_episode(index)
        return

    @override
    def onClick(self, control_id):
        if control_id == EpisodesDialog.XML_ID_BTN_SEASON:
            self.__on_download_season()
        return

    def __on_hover_episode(self, index):
        lst = self.getControlList(EpisodesDialog.XML_ID_LIST_FAKE)
        lst.reset()
        episode = self.__episodes[index]
        lst.addItem(episode.to_list_item())
        return

    def __on_download_season(self):
        if self.__season.is_downloadable() is False:
            xbmcgui.Dialog().ok(addon.ADDON.getLocalizedString(30005), addon.ADDON.getLocalizedString(30006))
            return
        dialog = TorrentsDialog.get_instance(self.__season.get_download_torrents())
        torrent = dialog.doModalSeason(self.__season)
        self.__service.request_download_show(torrent.get_id(),
                                             season_no=self.__season.get_season_no())
        del dialog
        return

    def __on_download(self, index):
        episode = self.__episodes[index]
        if episode.is_downloadable() is False:
            xbmcgui.Dialog().ok(addon.ADDON.getLocalizedString(30005), addon.ADDON.getLocalizedString(30007))
            return
        dialog = TorrentsDialog.get_instance(episode.get_download_torrents())
        torrent = dialog.doModalEpisode(episode)
        self.__service.request_download_show(torrent.get_id(),
                                             season_no=self.__season.get_season_no(),
                                             episode_no=episode.get_episode_number())
        del dialog
        return

    @staticmethod
    def __panel_item(episode):
        item = xbmcgui.ListItem(str(episode.get_episode_number()))
        item.setProperty("IsDownloadable", str(episode.is_downloadable()))
        return item
