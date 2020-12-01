import xbmcgui
from lib import addon
from lib.utils.logger import Logger
from window import Window


class VideosDialog(xbmcgui.WindowXMLDialog, Window):
    _logger = Logger.get_instance(__name__)

    XML_ID_LIST = 250

    @classmethod
    def get_instance(cls, videos_lst):
        return VideosDialog('script-videos_dialog.xml', addon.ADDON_PATH, 'default', '1080i',
                            videos_lst=videos_lst)

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self, args[0], args[1], args[2], args[3])
        Window.__init__(self)
        self._video_lst = kwargs['videos_lst']
        self._selection_media = None
        return

    def doModal(self):
        if self._video_lst is None or len(self._video_lst) == 0:
            xbmcgui.Dialog().ok(addon.ADDON.getLocalizedString(30003), addon.ADDON.getLocalizedString(30004))
            return None
        xbmcgui.WindowXMLDialog.doModal(self)
        return self._selection_media

    def onInit(self):
        lst = self.getControlList(VideosDialog.XML_ID_LIST)
        if lst.size() == 0:
            self._render()
        return

    def _render(self):
        lst = self.getControlList(VideosDialog.XML_ID_LIST)
        if self._video_lst is not None:
            items = []
            for video in self._video_lst:
                items.append(video.to_list_item())
            lst.addItems(items)
            self.setFocusId(VideosDialog.XML_ID_LIST)
        return

    def onAction(self, action):
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            self._selection_media = None
            self.close()
        if action.getId() == xbmcgui.ACTION_SELECT_ITEM and self.getFocusId() == VideosDialog.XML_ID_LIST:
            index = self.getControlList(VideosDialog.XML_ID_LIST).getSelectedPosition()
            self._selection_media = self._video_lst[index]
            self.close()
        return

    def size(self):
        if self._video_lst is None:
            return 0
        return len(self._video_lst)
