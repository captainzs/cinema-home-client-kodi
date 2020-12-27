import datetime

import xbmc
from lib.gui.items.episode_list_item import EpisodeListItem
from lib.models.json.image_info import Image
from lib.models.json.torrent_info import Torrent
from lib.utils import lst_sorter


class Episode:
    @classmethod
    def of(cls, season, json):
        return Episode(season, json)

    def __init__(self, season, json):
        self.__season = season
        self.__json = json
        return

    def to_list_item(self):
        return EpisodeListItem.of(self)

    def get__season(self):
        return self.__season

    def get_episode_number(self):
        number = self.__json.get("episodeNumber", None)
        return int(number) if number is not None else None

    def get_name(self):
        all_names = self.__json.get("names")
        if all_names is None or len(all_names) == 0:
            return None
        return lst_sorter.sort_locale_texts(all_names, [xbmc.getLanguage(xbmc.ISO_639_1), "en"])[0]

    def get_plot(self):
        all_plots = self.__json.get("plots")
        if all_plots is None or len(all_plots) == 0:
            return None
        return lst_sorter.sort_locale_texts(all_plots, [xbmc.getLanguage(xbmc.ISO_639_1), "en"])[0]

    def get_rating(self):
        return self.__json.get("rating")

    def get_air_date(self):
        date_str = self.__json.get("airDate", None)
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if date_str else None

    def get_posters(self):
        return self.__season.get_posters()

    def get_stills(self):
        stills = lst_sorter.sort_arts([Image.of(i_json) for i_json in self.__json.get("stills", [])],
                                      [None, xbmc.getLanguage(xbmc.ISO_639_1), "en"])
        stills.extend(self.__season.get_backdrops())
        return stills

    def get_torrents(self):
        return [Torrent.of(t) for t in self.__json.get("torrents", [])]

    def get_download_torrents(self):
        torrents = self.get_torrents()
        torrents.extend(self.__season.get_download_torrents())
        return torrents

    def is_available(self):
        return len(self.get_torrents()) > 0

    def is_downloadable(self):
        if self.is_available() is True:
            return True
        if self.__season.is_downloadable():
            return True
        return False
