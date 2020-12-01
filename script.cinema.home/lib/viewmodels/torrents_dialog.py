import xbmcgui
from lib import addon
from lib.utils.logger import Logger
from window import Window


class TorrentsDialog(xbmcgui.WindowXMLDialog, Window):
    _logger = Logger.get_instance(__name__)

    XML_ID_BTN_DOWNLOAD = 11
    XML_ID_BTN_RELEASES = 12
    XML_ID_BTN_CANCEL = 13
    XML_ID_LIST = 110

    XML_PROP_ON_RELEASES = "OnShowAll"
    XML_PROP_MEDIA_LABEL = "MediaPieceLabel"

    @classmethod
    def get_instance(cls, torrents):
        return TorrentsDialog('script-torrent_dialog.xml', addon.ADDON_PATH, 'default', '1080i',
                              torrents=torrents)

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self, args[0], args[1], args[2], args[3])
        Window.__init__(self)
        self._torrents = kwargs['torrents']
        self._selected_index = None
        return

    def doModal(self):
        self.setProperty(TorrentsDialog.XML_PROP_MEDIA_LABEL, "All")
        self._do_modal()
        return

    # noinspection PyPep8Naming
    def doModalSeason(self, season):
        self.setProperty(TorrentsDialog.XML_PROP_MEDIA_LABEL, "Season {}".format(season.get_season_no()))
        self._do_modal()
        return

    # noinspection PyPep8Naming
    def doModalEpisode(self, episode):
        self.setProperty(TorrentsDialog.XML_PROP_MEDIA_LABEL, "Episode {}".format(episode.get_episode_number()))
        self._do_modal()
        return

    def _do_modal(self):
        if self._torrents is None or len(self._torrents) == 0:
            xbmcgui.Dialog().ok(addon.ADDON.getLocalizedString(30005), addon.ADDON.getLocalizedString(30012))
            return
        self._selected_index = 0
        xbmcgui.WindowXMLDialog.doModal(self)
        return

    def onInit(self):
        lst = self.getControlList(TorrentsDialog.XML_ID_LIST)
        lst.addItems([t.to_list_item() for t in self._torrents])
        self.setFocusId(TorrentsDialog.XML_ID_BTN_CANCEL)
        return

    def onAction(self, action):
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            if self.getFocusId() == TorrentsDialog.XML_ID_LIST:
                self.getControlList(TorrentsDialog.XML_ID_LIST).selectItem(self._selected_index)
                self.clearProperty(TorrentsDialog.XML_PROP_ON_RELEASES)
                self.setFocusId(TorrentsDialog.XML_ID_BTN_RELEASES)
            else:
                self.close()
        elif action.getId() == xbmcgui.ACTION_SELECT_ITEM:
            if self.getFocusId() == TorrentsDialog.XML_ID_LIST:
                self._selected_index = self.getControlList(TorrentsDialog.XML_ID_LIST).getSelectedPosition()
                self.clearProperty(TorrentsDialog.XML_PROP_ON_RELEASES)
                self.setFocusId(TorrentsDialog.XML_ID_BTN_DOWNLOAD)
        return

    def onClick(self, control_id):
        if control_id == TorrentsDialog.XML_ID_BTN_RELEASES:
            self.setFocusId(TorrentsDialog.XML_ID_LIST)
        return

    def size(self):
        if self._torrents is None:
            return 0
        return len(self._torrents)
