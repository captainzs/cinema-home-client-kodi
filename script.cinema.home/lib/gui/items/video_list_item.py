import xbmc
import xbmcgui
from lib.services.file_downloader import try_download_thumb
from lib.utils.logger import Logger


class VideoListItem(xbmcgui.ListItem):
    _logger = Logger.get_instance(__name__)

    @classmethod
    def of(cls, video):
        item = VideoListItem()
        item.init(video)
        return item

    def __init__(self):
        xbmcgui.ListItem.__init__(self)
        self.setInfo("video", {"mediatype": "video"})
        return

    def init(self, video):
        title = video.get_title()
        if title:
            self.setInfo("video", {"title": title})
        thumb = try_download_thumb(video.get_url())
        if thumb:
            self.setArt({'thumb': thumb})
        video_type = video.get_type()
        if video_type:
            self.setProperty("Type", video_type)
        iso639 = video.get_iso639()
        if iso639:
            self.addStreamInfo('audio', {'language': xbmc.convertLanguage(iso639, xbmc.ENGLISH_NAME)})
        return
