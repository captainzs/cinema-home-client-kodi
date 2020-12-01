from lib.models.art import Art
from lib.utils.override import override


class Image(Art):
    @classmethod
    def of(cls, json):
        return Image(json)

    def __init__(self, json):
        Art.__init__(self)
        self.__json = json
        return

    @override
    def get_url(self):
        return self.__json.get("url", None)

    @override
    def get_iso639(self):
        return self.__json.get("iso639Id", None)

    def __repr__(self):
        return str(self.__json)
