import xbmc
import xbmcgui
from lib.services.file_downloader import try_download_one
from lib.utils import interpreter
from lib.utils.logger import Logger


class MediaListItem(xbmcgui.ListItem):
    __logger = Logger.get_instance(__name__)

    def __init__(self, media_type):
        xbmcgui.ListItem.__init__(self, media_type)
        self.setInfo("video", {"mediatype": media_type})
        self.__media = None
        return

    def get_media(self):
        return self.__media

    def has_poster(self):
        return len(self.getArt("poster")) > 0

    def init(self, media):
        self.__media = media
        self.setUniqueIDs({'imdb': media.get_imdb_id(), 'tmdb': media.get_tmdb_id()}, "imdb")
        title = media.get_title()
        if title:
            self.setInfo("video", {"title": title.get("str")})
        plot = media.get_plot()
        if plot:
            self.setInfo("video", {"plot": plot.get("str")})
        meta_line = []
        rating = media.get_rating()
        if rating:
            meta_line.append(str(round(rating, 1)))
            self.setRating("averaged", rating)
        year = media.get_year()
        if year:
            meta_line.append(str(year))
            self.setInfo("video", {"year": year})
        minutes = media.get_runtime_mins()
        if minutes:
            meta_line.append(interpreter.duration_2_readable(minutes * 60))
            self.setInfo("video", {"duration": minutes * 60})
        if len(meta_line) > 0:
            self.setProperty("MetaLine", "   ".join(meta_line))

        backdrop = try_download_one(media.get_backdrops())
        if backdrop:
            self.setArt({"landscape": backdrop.get_path()})
        logo = try_download_one(media.get_logos())
        if logo:
            self.setArt({"clearlogo": logo.get_path()})
        poster = try_download_one(media.get_posters())
        if poster:
            self.setArt({'poster': poster.get_path()})
        thumb = try_download_one(media.get_thumbs())
        if thumb:
            self.setArt({'thumb': thumb.get_path()})
        elif backdrop:
            self.setArt({'thumb': backdrop.get_path()})

        title_translated = title is not None and title.get("iso639Id", None) == xbmc.getLanguage(xbmc.ISO_639_1)
        logo_translated = logo is not None and logo.get_iso639() == xbmc.getLanguage(xbmc.ISO_639_1)
        self.setProperty("TranslatedTitleNeeded",
                         str(title_translated is True and logo_translated is False and logo is not None))

        creators = media.get_creators(2)
        if creators:
            self.setProperty("Creators", ", ".join(creators))
        actors = media.get_actors(3)
        if actors:
            self.setProperty("Actors", ", ".join([a.get("name") for a in actors]))
        genres = media.get_genres(4)
        if genres:
            self.setProperty("Genres", ", ".join([g.name for g in genres]))
        videos = media.get_videos()
        if videos:
            self.setProperty("VideosNo", str(len(videos)))
        else:
            self.setProperty("VideosNo", str(0))
        self.setProperty("IsAvailable", str(media.is_available()))
        collection = media.get_collection()
        if collection:
            self.setProperty("HasCollection", str(True))
        network = media.get_network()
        if network is not None:
            self.setProperty("NetworkFileName", network.file)
        return
