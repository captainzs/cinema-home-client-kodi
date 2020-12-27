from lib.gui.items.torrent_list_item import TorrentListItem
from lib.utils.override import override


class Torrent:
    @classmethod
    def of(cls, json):
        return Torrent(json)

    def __init__(self, json):
        self.__json = json
        return

    def to_list_item(self):
        return TorrentListItem.of(self)

    def get_id(self):
        return self.__json.get("id")

    def get_title(self):
        return self.__json.get("title")

    def get_unique_language(self):
        languages = self.get_languages()
        if 0 in languages:
            return 0
        if 1 in languages:
            languages.remove(1)
            languages.append(1)
        return languages[0]

    def get_languages(self):
        return self.__json.get("release").get("audioLanguages")

    def get_size(self):
        return self.__json.get("release").get("fullSize")

    def get_res_def(self):
        return self.__json.get("release").get("resolutionDefinition")

    def get_res(self):
        return self.__json.get("release").get("resolution")

    def get_audio_channels(self):
        return self.__json.get("release").get("audioChannels")

    def get_sources(self):
        return self.__json.get("release").get("sources")

    def get_video_codec(self):
        return self.__json.get("release").get("videoCodec")

    def get_audio_codecs(self):
        return self.__json.get("release").get("audioCodecs")

    def get_color_codec(self):
        return self.__json.get("release").get("colorCodec")

    def is_hdr(self):
        return self.__json.get("release").get("hdr")

    def is_3d(self):
        return self.__json.get("release").get("3d")

    def is_widescreen(self):
        return self.__json.get("release").get("widescreen")

    def is_hardcoded(self):
        return self.__json.get("release").get("hardcoded")

    def is_black_white(self):
        return self.__json.get("release").get("blackAndWhite")

    def get_seeds(self):
        return int(self.__json.get("seeds", "0"))

    def get_leechers(self):
        return int(self.__json.get("leechers", "0"))

    def get_peers(self):
        return self.get_seeds() + self.get_leechers()

    @override
    def __eq__(self, other):
        if isinstance(other, Torrent):
            return self.get_id() == other.get_id()
        return False

    @override
    def __ne__(self, other):
        return not self.__eq__(other)

    @override
    def __hash__(self):
        return hash(self.get_id())
