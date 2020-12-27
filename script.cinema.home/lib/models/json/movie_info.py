import xbmc
from lib.gui.items.movie_list_item import MovieListItem
from lib.models.json.media_info import MediaNfo
from lib.models.json.torrent_info import Torrent
from lib.models.types.media_type import MediaType, MediaLevel
from lib.utils import lst_sorter
from lib.utils.logger import Logger
from lib.utils.merger import merge


class MovieNfo(MediaNfo):
    __logger = Logger.get_instance(__name__)

    @classmethod
    def of(cls, json, level=MediaLevel.SIMPLE):
        return MovieNfo(json, level=level)

    @classmethod
    def merged(cls, movie1, movie2):
        json1 = movie1.get_json()
        json2 = movie2.get_json()
        return MovieNfo(merge(json1, json2), level=max(movie1.get_level(), movie2.get_level()))

    def __init__(self, json, level):
        MediaNfo.__init__(self, MediaType.MOVIE, json, level)
        return

    def to_list_item(self):
        return MovieListItem.of(self)

    def get_tagline(self):
        all_lines = self.get_json().get("taglines")
        if all_lines is None or len(all_lines) == 0:
            return None
        return lst_sorter.sort_locale_texts(all_lines, [xbmc.getLanguage(xbmc.ISO_639_1)])[0]

    def get_torrents(self):
        torrents = self.get_json().get("torrents")
        if torrents is None or len(torrents) == 0:
            return None
        return [Torrent.of(t) for t in torrents]

    def is_available(self):
        torrents = self.get_json().get("torrents")
        if torrents is None or len(torrents) == 0:
            return False
        return True

    def __repr__(self):
        return str(self.get_json())
