import logging
import os
from logging.handlers import RotatingFileHandler

import xbmc
from lib import addon


class Logger:
    PREFIX = "[CINEMA-HOME] "

    @classmethod
    def get_instance(cls, name):
        return Logger(name)

    @staticmethod
    def get_log_path():
        return os.path.join(addon.ADDON_DATA_PATH, "cinema.home.log")

    def __init__(self, name):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        handler = RotatingFileHandler(self.get_log_path(), maxBytes=80000, backupCount=10, encoding="utf-8",
                                      delay=False)
        handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s:%(lineno)d - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        return

    def debug(self, message):
        message_u = unicode(message)
        message_b = (self.PREFIX + message_u).encode("utf-8")
        xbmc.log(msg=message_b, level=xbmc.LOGDEBUG)
        self.logger.debug(message_u)
        return

    def info(self, message):
        message_u = unicode(message)
        message_b = (self.PREFIX + message_u).encode("utf-8")
        xbmc.log(msg=message_b, level=xbmc.LOGINFO)
        self.logger.info(message_u)
        return

    def warning(self, message):
        message_u = unicode(message)
        message_b = (self.PREFIX + message_u).encode("utf-8")
        xbmc.log(msg=message_b, level=xbmc.LOGWARNING)
        self.logger.warning(message_u)
        return

    def error(self, message):
        message_u = unicode(message)
        message_b = (self.PREFIX + message_u).encode("utf-8")
        xbmc.log(msg=message_b, level=xbmc.LOGERROR)
        self.logger.error(message_u)
        return

    def exception(self, message):
        message_u = unicode(message)
        message_b = (self.PREFIX + message_u).encode("utf-8")
        xbmc.log(msg=message_b, level=xbmc.LOGERROR)
        self.logger.exception(message_u)
        return

    def close(self):
        if self.logger:
            handlers = self.logger.handlers[:]
            for handler in handlers:
                handler.close()
                self.logger.removeHandler(handler)
