from abc import ABCMeta, abstractmethod

from lib.gui.items.media_set_list_item import MediaSetPageListItem
from lib.services.client_service import ClientService


class MediaSet:
    __metaclass__ = ABCMeta

    def __init__(self, media_type, client_service=ClientService.get_instance()):
        self._media_type = media_type
        self.__client_service = client_service
        self.__medias_2_page = {}
        self.__id_set = set()
        return

    def to_list_item(self, page_no):
        return MediaSetPageListItem.of(self, page_no)

    def page(self, page_no):
        if page_no is None:
            return None
        page = self.__medias_2_page.get(page_no)
        if page is None:
            page = self.__client_service.request_lst(self.get_path(1), self.get_body(), self.get_media_type())
            self.__extend(page_no, page)
        return page

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

    def __extend(self, page_no, new_page):
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
