import xbmc
from lib.gui.items.season_list_item import SeasonListItem
from lib.models.episode_info import Episode
from lib.models.image_info import Image
from lib.models.torrent_info import Torrent
from lib.utils import lst_sorter


class Season:
    @classmethod
    def of(cls, show, json):
        return Season(show, json)

    def __init__(self, show, json):
        self.__show = show
        self.__json = json
        return

    def to_list_item(self):
        return SeasonListItem.of(self)

    def get_show(self):
        return self.__show

    def get_season_no(self):
        return self.__json.get("seasonNumber")

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

    def get_release_year(self):
        air_date = self.__json.get("airDate")
        if air_date is None:
            return None
        return air_date[0:4]

    def get_air_date(self):
        return self.__json.get("airDate")

    def get_episode_count(self):
        count = self.__json.get("episodeCount")
        if count is None:
            return None
        return int(count)

    def get_episodes(self):
        return lst_sorter.sort_episodes([Episode.of(self, e) for e in self.__json.get("episodes", [])])

    def get_posters(self):
        posters = lst_sorter.sort_arts([Image.of(i_json) for i_json in self.__json.get("posters", [])],
                                       [xbmc.getLanguage(xbmc.ISO_639_1), "en"])
        posters.extend(self.__show.get_posters())
        return posters

    def get_backdrops(self):
        return self.__show.get_backdrops()

    def get_logos(self):
        return self.__show.get_logos()

    def get_thumbs(self):
        return self.__show.get_thumbs()

    def get_torrents(self):
        return [Torrent.of(t) for t in self.__json.get("torrents", [])]

    def get_download_torrents(self):
        torrents = self.get_torrents()
        torrents.extend(self.__show.get_download_torrents())
        return torrents

    def is_available(self):
        if len(self.get_torrents()) > 0:
            return True
        for episode in self.get_episodes():
            if episode.is_available():
                return True
        return False

    def is_downloadable(self):
        if len(self.get_torrents()) > 0:
            return True
        if self.__show.is_downloadable():
            return True
        return False
