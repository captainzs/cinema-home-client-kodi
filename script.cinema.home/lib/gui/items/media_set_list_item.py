import xbmcgui


class MediaSetPageListItem(xbmcgui.ListItem):
    @classmethod
    def of(cls, media_set, page_no):
        item = MediaSetPageListItem()
        item.init(media_set, page_no)
        return item

    def __init__(self):
        xbmcgui.ListItem.__init__(self)
        self.__media_set = None
        self.__items = []
        self.__selected = None
        return

    def init(self, media_set, page_no):
        self.__media_set = media_set
        for media in media_set.page(page_no):
            item = media.to_list_item()
            if item.has_poster():
                self.__items.append(item)
        return

    def get_set(self):
        return self.__media_set

    def get_name(self):
        return self.__media_set.get_name()

    def get_items(self):
        return self.__items

    def is_empty(self):
        return len(self.__items) == 0

    def get_selected_item(self):
        if self.__selected is None:
            return None
        return self.__items[self.__selected]

    def set_selected_position(self, selected):
        self.__selected = selected
        return

    def get_selected_position(self):
        return self.__selected
