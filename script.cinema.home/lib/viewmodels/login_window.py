import xbmcgui
from lib import addon
from lib.utils.logger import Logger
from lib.viewmodels.details_window import DetailsWindow
from lib.viewmodels.menu_main_dialog import MenuMainDialog
from window import Window


class LogInWindow(xbmcgui.WindowXML, Window):
    _logger = Logger.get_instance(__name__)

    @classmethod
    def get_instance(cls):
        return LogInWindow('script-login_window.xml', addon.ADDON_PATH, 'default', '1080i', True)

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXML.__init__(self, args[0], args[1], args[2], args[3], args[4])
        Window.__init__(self)
        self.__logged_in = False
        return

    def onInit(self):
        if self.__logged_in is False:
            self.__logged_in = True
            dialog = MenuMainDialog.get_instance()
            dialog.load_movies_menu()
            window = DetailsWindow.get_instance()
            window.doModalBrowser(dialog)
            self.close()
        return

    def onAction(self, action):
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            self.close()
        return
