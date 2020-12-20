import xbmcgui
from lib.services import file_downloader
from lib.utils.logger import Logger


class EpisodeListItem(xbmcgui.ListItem):
    _logger = Logger.get_instance(__name__)

    @classmethod
    def of(cls, episode):
        item = EpisodeListItem()
        item.init(episode)
        return item

    def __init__(self):
        xbmcgui.ListItem.__init__(self)
        self.setInfo("video", {"mediatype": "episode"})
        return

    def init(self, episode):
        name = episode.get_name()
        if name:
            self.setInfo("video", {"title": name.get("str")})
        plot = episode.get_plot()
        if plot:
            self.setInfo("video", {"plot": plot.get("str")})
        self.setInfo("video", {"episode": str(episode.get_episode_number())})
        rating = episode.get_rating()
        if rating:
            self.setRating("averaged", rating)
        aired = episode.get_air_date()
        if aired:
            self.setProperty("Aired", str(aired))
        self.setProperty("IsDownloadable", str(episode.is_downloadable()))

        still = file_downloader.try_download_one(episode.get_stills())
        if still:
            self.setArt({'thumb': still.get_path()})
        poster = file_downloader.try_download_one(episode.get_posters())
        if poster:
            self.setArt({'poster': poster.get_path()})
        return
