from lib.gui.items.media_list_item import MediaListItem
from lib.utils import interpreter
from lib.utils.logger import Logger


class ShowListItem(MediaListItem):
    _logger = Logger.get_instance(__name__)

    @classmethod
    def of(cls, show):
        item = ShowListItem()
        item.init(show)
        return item

    def __init__(self):
        MediaListItem.__init__(self, "tvshow")
        return

    def init(self, show):
        MediaListItem.init(self, show)
        tagline = show.get_tagline()
        if tagline:
            self.setInfo("video", {"tagline": tagline})
        status = show.get_status()
        if status is not None:
            self.setInfo("video", {"status": interpreter.show_status_2_readable(status)})
        return
