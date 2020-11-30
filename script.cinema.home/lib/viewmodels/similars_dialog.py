import xbmcgui
from lib import addon
from lib.utils.logger import Logger
from window import Window


class SimilarsDialog(xbmcgui.WindowXMLDialog, Window):
    _logger = Logger.get_instance(__name__)

    XML_ID_LIST = 150

    @classmethod
    def get_instance(cls, media_lst):
        return SimilarsDialog('script-similars_dialog.xml', addon.ADDON_PATH, 'default', '1080i',
                              media_lst=media_lst)

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXMLDialog.__init__(self, args[0], args[1], args[2], args[3])
        Window.__init__(self)
        self.__media_lst = kwargs['media_lst']
        self._selected_media = None
        return

    def doModal(self):
        if self.__media_lst is None or len(self.__media_lst) == 0:
            xbmcgui.Dialog().ok(addon.ADDON.getLocalizedString(30003), addon.ADDON.getLocalizedString(30011))
            return None
        Window.doModal(self)
        return self._selected_media

    def onInit(self):
        lst = self.getControlList(SimilarsDialog.XML_ID_LIST)
        if lst.size() == 0:
            self._render()
        return

    def _render(self):
        if self.__media_lst is None or len(self.__media_lst) == 0:
            return
        lst = self.getControlList(SimilarsDialog.XML_ID_LIST)
        lst.addItems([media.to_list_item() for media in self.__media_lst])
        self.setFocusId(SimilarsDialog.XML_ID_LIST)
        return

    def onAction(self, action):
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            self._selected_media = None
            self.close()
        elif action.getId() == xbmcgui.ACTION_SELECT_ITEM and self.getFocusId() == SimilarsDialog.XML_ID_LIST:
            selected_index = self.getControlList(SimilarsDialog.XML_ID_LIST).getSelectedPosition()
            selected_media = self.__media_lst[selected_index]
            if selected_media.is_available() is True:
                self._selected_media = selected_media
                self.close()
            else:
                xbmcgui.Dialog().ok(addon.ADDON.getLocalizedString(30005), addon.ADDON.getLocalizedString(30012))
        return

    def size(self):
        if self.__media_lst is None:
            return 0
        return len(self.__media_lst)
