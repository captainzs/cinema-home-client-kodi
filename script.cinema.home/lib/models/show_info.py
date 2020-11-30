from lib.gui.items.show_list_item import ShowListItem
from lib.models.episode_info import Episode
from lib.models.media_info import MediaNfo
from lib.models.season_info import Season
from lib.models.torrent_info import Torrent
from lib.models.types.media_type import MediaType, MediaLevel
from lib.utils import lst_sorter, tagliner
from lib.utils.logger import Logger
from lib.utils.merger import merge


class ShowNfo(MediaNfo):
    __logger = Logger.get_instance(__name__)

    @classmethod
    def of(cls, json, level=MediaLevel.SIMPLE):
        return ShowNfo(json, level=level)

    @classmethod
    def merged(cls, show1, show2):
        json1 = show1.get_json()
        json2 = show2.get_json()
        return ShowNfo(merge(json1, json2), level=max(show1.get_level(), show2.get_level()))

    def __init__(self, json, level):
        MediaNfo.__init__(self, MediaType.SHOW, json, level)
        return

    def to_list_item(self):
        return ShowListItem.of(self)

    def get_next_episode(self):
        episode = self.get_json().get("nextEpisode", None)
        return Episode.of(None, episode) if episode else None

    def get_seasons(self):
        return lst_sorter.sort_seasons([Season.of(self, s) for s in self.get_json().get("seasons", [])])

    def get_tagline(self):
        return tagliner.to_tagline(self.get_next_episode())

    def get_all_torrents(self):
        all_torrents = self.get_torrents()
        for season in self.get_seasons():
            all_torrents.extend(season.get_torrents())
            for episode in season.get_episodes():
                all_torrents.extend(episode.get_torrents())
        return lst_sorter.sort_torrents(set(all_torrents))

    def get_torrents(self):
        torrents = self.get_json().get("completeTorrents", [])
        torrents.extend(self.get_json().get("unassignedTorrents", []))
        return [Torrent.of(t) for t in torrents]

    def get_download_torrents(self):
        return [Torrent.of(t) for t in self.get_json().get("completeTorrents", [])]

    def is_available(self):
        if len(self.get_torrents()) > 0:
            return True
        for season in self.get_seasons():
            if season.is_available():
                return True
        return False

    def is_downloadable(self):
        return len(self.get_json().get("completeTorrents", [])) > 0

    def __repr__(self):
        return str(self.get_json())
