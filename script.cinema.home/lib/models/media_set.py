from abc import ABCMeta, abstractmethod

from lib.gui.items.media_set_list_item import MediaSetListItem


class MediaSet:
    __metaclass__ = ABCMeta

    def __init__(self, media_type):
        self._media_type = media_type
        self.__medias_2_page = {}
        self.__id_set = set()
        return

    def to_list_item(self):
        return MediaSetListItem.of(self)

    def extend(self, page_no, new_page):
        if page_no is None or page_no < 1:
            return None
        if new_page is None:
            return None
        uniques = []
        for media in new_page:
            if media.get_imdb_id() not in self.__id_set:
                uniques.append(media)
                self.__id_set.add(media.get_imdb_id())
        if page_no not in self.__medias_2_page:
            self.__medias_2_page[page_no] = []
        self.__medias_2_page[page_no].extend(uniques)
        return uniques

    def page(self, page_no):
        if page_no is None:
            return None
        return self.__medias_2_page.get(page_no)

    def get_media(self, imdb_id):
        for page_no, page in self.__medias_2_page.items():
            for media in page:
                if media.get_imdb_id() == imdb_id:
                    return media
        return None

    def get_media_type(self):
        return self._media_type

    @abstractmethod
    def get_name(self):
        pass

    @abstractmethod
    def get_path(self, page):
        pass

    @abstractmethod
    def get_body(self):
        pass
