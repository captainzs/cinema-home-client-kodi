import requests

import xbmc
import xbmcgui
from lib.models.dynamic_data import DynamicData
from lib.models.movie_info import MovieNfo
from lib.models.show_info import ShowNfo
from lib.models.types.media_type import MediaType, MediaLevel
from lib.services.media_storage import MediaStorage
from lib.utils.logger import Logger


class ClientService:
    __logger = Logger.get_instance(__name__)

    @classmethod
    def get_instance(cls):
        return ClientService(MediaStorage())

    ADDRESS = "http://localhost:8080{}"
    HEADERS = {'Content-Type': 'application/json', 'Accept-Language': xbmc.getLanguage(xbmc.ISO_639_1)}

    def __init__(self, storage):
        self._storage = storage
        return

    @staticmethod
    def __request(path, json=None, data=None):
        try:
            return requests.post(ClientService.ADDRESS.format(path), json=json, data=data,
                                 headers=ClientService.HEADERS)
        except requests.ConnectionError:
            xbmcgui.Dialog().ok('Server error', "Cinema-Home server is not reachable!")
        return None

    def request_lst(self, path, json_body, media_type):
        all_nfos = []
        response = self.__request(path, json=json_body)
        if response:
            for json in response.json():
                media = MovieNfo.of(json) if media_type == MediaType.MOVIE else ShowNfo.of(json)
                all_nfos.append(self._storage.cache(media))
        return all_nfos

    def request_details(self, imdb_id, media_type):
        cached = self._storage.get(imdb_id)
        if cached is not None and cached.get_level() >= MediaLevel.DETAILED:
            return cached
        path_segment = "movie" if media_type == MediaType.MOVIE else "show"
        path = "/api/client/{}/{}".format(path_segment, imdb_id)
        response = self.__request(path)
        if response is None:
            return None
        if media_type == MediaType.MOVIE:
            media = MovieNfo.of(response.json(), MediaLevel.DETAILED)
        else:
            media = ShowNfo.of(response.json(), MediaLevel.DETAILED)
        return self._storage.cache(media)

    def request_movie_torrents(self, imdb_id):
        cached = self._storage.get(imdb_id)
        if cached is not None and cached.get_level() >= MediaLevel.DOWNLOADABLE:
            return cached
        path = "/api/client/torrents/movie/{}".format(imdb_id)
        response = self.__request(path)
        if response is None:
            return None
        return self._storage.cache(MovieNfo.of(response.json(), MediaLevel.DOWNLOADABLE))

    def request_show_torrents(self, imdb_id):
        cached = self._storage.get(imdb_id)
        if cached is not None and cached.get_level() >= MediaLevel.DOWNLOADABLE:
            return cached
        path = "/api/client/torrents/show/{}".format(imdb_id)
        response = self.__request(path)
        if response is None:
            return None
        self._storage.cache(ShowNfo.of(response.json(), MediaLevel.DOWNLOADABLE))

    def report(self, imdb_id, message):
        path = "/api/client/report/{}".format(imdb_id)
        self.__request(path, data=message)
        return

    def request_dynamic_data(self, imdb_id):
        path = "/api/client/data/{}".format(imdb_id)
        response = self.__request(path)
        if response is None:
            return None
        return DynamicData(response.json())
