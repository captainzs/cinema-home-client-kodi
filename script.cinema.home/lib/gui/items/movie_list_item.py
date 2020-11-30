from lib.gui.items.media_list_item import MediaListItem


class MovieListItem(MediaListItem):
    @classmethod
    def of(cls, movie):
        item = MovieListItem()
        item.init(movie)
        return item

    def __init__(self):
        MediaListItem.__init__(self, "movie")
        return

    def init(self, movie):
        MediaListItem.init(self, movie)
        tagline = movie.get_tagline()
        if tagline:
            self.setInfo("video", {"tagline": tagline.get("str")})
        return
