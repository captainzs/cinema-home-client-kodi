from lib.gui.items.video_list_item import VideoListItem
from lib.models.art import Art
from lib.utils.override import override


class Video(Art):
    @classmethod
    def of(cls, json):
        return Video(json)

    def __init__(self, json):
        Art.__init__(self)
        self._json = json
        self.thumb = None
        return

    @override
    def to_list_item(self):
        return VideoListItem.of(self)

    @override
    def get_url(self):
        return self._json.get("url")

    @override
    def get_iso639(self):
        return self._json.get("iso639Id")

    def get_title(self):
        return self._json.get("title")

    def get_type(self):
        return self._json.get("type")
