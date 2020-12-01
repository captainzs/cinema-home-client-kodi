import os
from abc import ABCMeta, abstractmethod


class Art:
    __metaclass__ = ABCMeta

    def __init__(self):
        self.__path = None
        return

    @abstractmethod
    def get_iso639(self):
        pass

    @abstractmethod
    def get_url(self):
        pass

    def is_available(self):
        return self.__path is not None and os.path.exists(self.__path)

    def get_path(self):
        return self.__path

    def set_path(self, path):
        self.__path = path
        return
