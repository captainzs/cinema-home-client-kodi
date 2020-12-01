from lib.models.media_set import MediaSet
from lib.models.types.media_type import MediaType
from lib.utils.override import override


class Recommended(MediaSet):
    @classmethod
    def movies_by_staff(cls):
        return Recommended(MediaType.MOVIE)

    @classmethod
    def shows_by_staff(cls):
        return Recommended(MediaType.SHOW)

    @classmethod
    def by_movie(cls, title, tmdb_id):
        return Recommended(MediaType.MOVIE, title, tmdb_id)

    @classmethod
    def by_show(cls, title, tmdb_id):
        return Recommended(MediaType.SHOW, title, tmdb_id)

    def __init__(self, media_type, title=None, tmdb_id=None):
        MediaSet.__init__(self, media_type)
        self._title = title
        self._tmdb_id = tmdb_id
        return

    @override
    def get_name(self):
        if self._tmdb_id is None:
            return "Editor's choice"
        else:
            return "Because you liked: {}".format(self._title)

    @override
    def get_path(self, page):
        path_segment = "movies" if self._media_type == MediaType.MOVIE else "shows"
        if self._tmdb_id is None:
            return "/api/client/recommend/{}?page={}".format(path_segment, page)
        else:
            return "/api/client/recommend/{}/{}?page={}".format(path_segment, self._tmdb_id, page)

    @override
    def get_body(self):
        return None


class Popular(MediaSet):
    @classmethod
    def movies(cls):
        return Popular(MediaType.MOVIE)

    @classmethod
    def shows(cls):
        return Popular(MediaType.SHOW)

    def __init__(self, media_type):
        MediaSet.__init__(self, media_type)
        return

    @override
    def get_name(self):
        return "Currently popular"

    @override
    def get_path(self, page):
        path_segment = "movies" if self._media_type == MediaType.MOVIE else "shows"
        return "/api/client/search/{}?page={}".format(path_segment, page)

    @override
    def get_body(self):
        return {"sortBy": "POPULARITY", "sortOrder": "DESCENDING"}


class Similar(MediaSet):
    @classmethod
    def to_movie(cls, name, tmdb_id):
        return Similar(MediaType.MOVIE, name, tmdb_id)

    @classmethod
    def to_show(cls, name, tmdb_id):
        return Similar(MediaType.SHOW, name, tmdb_id)

    def __init__(self, media_type, name, tmdb_id):
        MediaSet.__init__(self, media_type)
        self._name = name
        self._tmdb_id = tmdb_id
        return

    @override
    def get_name(self):
        return "Because you downloaded: {}".format(self._name)

    @override
    def get_path(self, page):
        path_segment = "movies" if self._media_type == MediaType.MOVIE else "shows"
        return "/api/client/similar/{}?id={}&page={}".format(path_segment, self._tmdb_id, page)

    @override
    def get_body(self):
        return None


class Categorized(MediaSet):
    @classmethod
    def movies_by_genre(cls, genre):
        return Categorized(MediaType.MOVIE, genre)

    @classmethod
    def shows_by_genre(cls, genre):
        return Categorized(MediaType.SHOW, genre)

    def __init__(self, media_type, genre):
        MediaSet.__init__(self, media_type)
        self._genre = genre
        return

    @override
    def get_name(self):
        label = "movies" if self._media_type == MediaType.MOVIE else "shows"
        return "{} {}".format(self._genre.name, label)

    @override
    def get_path(self, page):
        path_segment = "movies" if self._media_type == MediaType.MOVIE else "shows"
        return "/api/client/search/{}?page={}".format(path_segment, page)

    @override
    def get_body(self):
        return {"genres": [self._genre.id], "sortBy": "POPULARITY", "sortOrder": "DESCENDING"}


class Newest(MediaSet):
    @classmethod
    def movies(cls):
        return Newest(MediaType.MOVIE)

    @classmethod
    def shows(cls):
        return Newest(MediaType.SHOW)

    def __init__(self, media_type):
        MediaSet.__init__(self, media_type)
        return

    @override
    def get_name(self):
        return "Newly added"

    @override
    def get_path(self, page):
        path_segment = "movies" if self._media_type == MediaType.MOVIE else "shows"
        return "/api/client/search/{}?page={}".format(path_segment, page)

    @override
    def get_body(self):
        return {"sortBy": "DATE", "sortOrder": "DESCENDING"}


class Best(MediaSet):
    @classmethod
    def movies(cls):
        return Best(MediaType.MOVIE)

    @classmethod
    def shows(cls):
        return Best(MediaType.SHOW)

    def __init__(self, media_type):
        MediaSet.__init__(self, media_type)
        return

    @override
    def get_name(self):
        return "Best of all time"

    @override
    def get_path(self, page):
        path_segment = "movies" if self._media_type == MediaType.MOVIE else "shows"
        return "/api/client/search/{}?page={}".format(path_segment, page)

    @override
    def get_body(self):
        return {"sortBy": "VIEWS", "sortOrder": "DESCENDING"}


class Streamed(MediaSet):
    @classmethod
    def movies_of(cls, network):
        return Streamed(MediaType.MOVIE, network)

    @classmethod
    def shows_of(cls, network):
        return Streamed(MediaType.SHOW, network)

    def __init__(self, media_type, network):
        MediaSet.__init__(self, media_type)
        self._network = network
        return

    @override
    def get_name(self):
        return "Popular on: {}".format(self._network.name)

    @override
    def get_path(self, page):
        path_segment = "movies" if self._media_type == MediaType.MOVIE else "shows"
        return "/api/client/search/{}/network/{}?page={}".format(path_segment, self._network.id, page)

    @override
    def get_body(self):
        return None


class Collection(MediaSet):
    @classmethod
    def of_movies(cls, collection):
        return Collection(MediaType.MOVIE, collection)

    @classmethod
    def of_shows(cls, collection):
        return Collection(MediaType.SHOW, collection)

    def __init__(self, media_type, collection):
        MediaSet.__init__(self, media_type)
        self._collection = collection
        return

    @override
    def get_name(self):
        return self._collection.get_name()

    @override
    def get_path(self, page):
        path_segment = "movies" if self._media_type == MediaType.MOVIE else "shows"
        return "/api/client/collection/{}?id={}".format(path_segment, self._collection.get_id())

    @override
    def get_body(self):
        return None
