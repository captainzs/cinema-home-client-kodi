from abc import abstractmethod

import xbmc
from lib.models.json.collection_info import Collection
from lib.models.json.image_info import Image
from lib.models.json.video_info import Video
from lib.models.types.genres import Genre
from lib.models.types.networks import Network
from lib.utils import lst_sorter
from lib.utils.logger import Logger


class MediaNfo:
    __logger = Logger.get_instance(__name__)

    def __init__(self, media_type, json, level):
        self.__media_type = media_type
        self.__json = json
        self.__level = level
        return

    def get_json(self):
        return self.__json

    def get_level(self):
        return self.__level

    def get_type(self):
        return self.__media_type

    def get_imdb_id(self):
        return self.__json.get("imdbId")

    def get_tmdb_id(self):
        return self.__json.get("tmdbId")

    def get_title(self):
        all_titles = self.__json.get("titles")
        if all_titles is None or len(all_titles) == 0:
            return None
        return lst_sorter.sort_locale_texts(all_titles, [xbmc.getLanguage(xbmc.ISO_639_1), "en"])[0]

    def get_plot(self):
        all_plots = self.__json.get("plots")
        if all_plots is None or len(all_plots) == 0:
            return None
        return lst_sorter.sort_locale_texts(all_plots, [xbmc.getLanguage(xbmc.ISO_639_1), "en"])[0]

    def get_rating(self):
        return self.__json.get("rating")

    def get_year(self):
        return self.__json.get("releaseYear")

    def get_runtime_mins(self):
        mins = self.__json.get("runtime")
        return int(mins) if mins is not None else None

    def get_posters(self):
        return lst_sorter.sort_arts([Image.of(i_json) for i_json in self.__json.get("posters", [])],
                                    [xbmc.getLanguage(xbmc.ISO_639_1), "en"])

    def get_backdrops(self):
        return lst_sorter.sort_arts([Image.of(i_json) for i_json in self.__json.get("backdrops", [])],
                                    [None, xbmc.getLanguage(xbmc.ISO_639_1), "en"])

    def get_logos(self):
        return lst_sorter.sort_arts([Image.of(i_json) for i_json in self.__json.get("logos", [])],
                                    [xbmc.getLanguage(xbmc.ISO_639_1), "en"])

    def get_thumbs(self):
        return lst_sorter.sort_arts([Image.of(i_json) for i_json in self.__json.get("thumbs", [])],
                                    [xbmc.getLanguage(xbmc.ISO_639_1), "en"])

    def get_videos(self):
        return lst_sorter.sort_videos([Video.of(v) for v in self.__json.get("videos", [])],
                                      [xbmc.getLanguage(xbmc.ISO_639_1), "en"])

    def get_actors(self, upper_limit=None):
        all_actors = self.__json.get("actors")
        if all_actors is None or len(all_actors) == 0:
            return None
        return_size = len(all_actors) if upper_limit is None else min(upper_limit, len(all_actors))
        return all_actors[:return_size]

    def get_genres(self, upper_limit=None):
        all_genres = self.__json.get("genres")
        if all_genres is None or len(all_genres) == 0:
            return None
        return_size = len(all_genres) if upper_limit is None else min(upper_limit, len(all_genres))
        return [Genre.of(g) for g in all_genres[:return_size]]

    def get_creators(self, upper_limit=None):
        all_creators = self.__json.get("creators")
        if all_creators is None or len(all_creators) == 0:
            return None
        return_size = len(all_creators) if upper_limit is None else min(upper_limit, len(all_creators))
        return all_creators[:return_size]

    def get_status(self):
        return self.__json.get("status")

    def get_collection(self):
        collection = self.__json.get("collection")
        if collection is None:
            return None
        return Collection(collection)

    def get_network(self):
        networks = self.__json.get("networks")
        if networks is None or len(networks) == 0:
            return None
        return Network.of(networks[0])

    @abstractmethod
    def is_available(self):
        pass
