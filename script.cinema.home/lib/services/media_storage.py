from lib.models.json.movie_info import MovieNfo
from lib.models.json.show_info import ShowNfo
from lib.models.types.media_type import MediaType
from lib.utils.logger import Logger


def singleton(cls, *args, **kw):
    instances = {}

    def _singleton():
        if cls not in instances:
            instances[cls] = cls(*args, **kw)
        return instances[cls]

    return _singleton


@singleton
class MediaStorage:
    __logger = Logger.get_instance(__name__)

    def __init__(self):
        self._media_2_id = {}
        return

    def cache(self, media):
        current = self._media_2_id.get(media.get_imdb_id(), None)
        if current is None:
            current = media
        else:
            current = self._merge(current, media)
        self._media_2_id[media.get_imdb_id()] = current
        return current

    def get(self, imdb_id):
        return self._media_2_id.get(imdb_id)

    @staticmethod
    def _merge(media1, media2):
        if media1.get_type() == MediaType.MOVIE and media2.get_type() == MediaType.MOVIE:
            return MovieNfo.merged(media1, media2)
        elif media1.get_type() == MediaType.SHOW and media2.get_type() == MediaType.SHOW:
            return ShowNfo.merged(media1, media2)
        else:
            raise Exception("Can not merge two different type of media!")
