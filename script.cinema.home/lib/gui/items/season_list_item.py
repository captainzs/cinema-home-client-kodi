import xbmc
import xbmcgui
from lib import addon
from lib.utils.logger import Logger


class SeasonListItem(xbmcgui.ListItem):
    _logger = Logger.get_instance(__name__)

    @classmethod
    def of(cls, season):
        item = SeasonListItem()
        item.init(season)
        return item

    def __init__(self):
        xbmcgui.ListItem.__init__(self)
        self.setInfo("video", {"mediatype": "season"})
        return

    def init(self, season):
        no = season.get_season_no()
        self.setProperty("SeasonNo", str(no))
        name = season.get_name()
        if name is not None:
            self.setInfo("video", {"title": name.get("str")})
        else:
            season_str = addon.ADDON.getLocalizedString(30000)
            if xbmc.getLanguage(xbmc.ISO_639_1) == "hu":
                self.setInfo("video", {"title": "{}. {}".format(no, season_str)})
            else:
                self.setInfo("video", {"title": "{} {}".format(season_str, no)})
        air_date = season.get_air_date()
        if air_date:
            self.setInfo("video", {"year": air_date[0:4]})
            self.setProperty("Aired", air_date)
        plot = season.get_plot()
        if plot:
            self.setInfo("video", {"plot": plot.get("str")})
        episodes_count = season.get_episode_count()
        if episodes_count:
            self.setProperty("EpisodesCount", str(episodes_count))
        self.setProperty("IsAvailable", str(season.is_available()))

        poster = try_download_one(season.get_posters())
        if poster:
            self.setArt({'poster': poster.get_path()})
        return
