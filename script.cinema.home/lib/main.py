from lib.utils.logger import Logger
from lib.viewmodels.login_window import LogInWindow


class Main:
    _logger = Logger.get_instance(__name__)

    def __init__(self):
        return

    def run(self):
        login_window = LogInWindow.get_instance()
        login_window.doModal()
        del login_window
        return
