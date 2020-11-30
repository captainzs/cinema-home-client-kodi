import datetime
import sys
import time

import youtube_dl
from lib.utils.logger import Logger


###############################################################################
# FIX: xbmcout instance in sys.stderr does not have isatty(), so we add it
###############################################################################
# TODO check hogy a kodnak melyik resze kell python2kodival es python3kodival, csak az fusson ami tenyleg kell


class StdErrWrapper(sys.stderr.__class__):
    def isatty(self):
        return False


sys.stderr.__class__ = StdErrWrapper

###############################################################################
# FIXES: datetime.datetime.strptime evaluating as None in Kodi
###############################################################################
# TODO amikor datetime error van akkor nem is lett redefinolva?!
_logger = Logger.get_instance(__name__)
try:
    datetime.datetime.strptime('0', '%H')
    _logger.debug("datetime.datetime works fine!")
except TypeError:
    def redefine_datetime(orig):
        class DatetimeWrapper(orig):
            @classmethod
            def strptime(cls, dstring, dformat):
                return datetime.datetime(*(time.strptime(dstring, dformat)[0:6]))

            def __repr__(self):
                return 'DatetimeWrapper.' + orig.__repr__(self)

        return DatetimeWrapper


    datetime.datetime = redefine_datetime(datetime.datetime)
    _logger.debug("datetime.datetime redefined!")


###############################################################################
# FIXES: overrides XBMC environment error causing methods
###############################################################################
class YoutubeDLWrapper(youtube_dl.YoutubeDL):
    _logger = Logger.get_instance(__name__)

    def __init__(self, *args, **kwargs):
        youtube_dl.YoutubeDL.__init__(self, *args, **kwargs)

    def get_thumb_url(self, url):
        info = self.extract_info(url, download=False, process=False)
        thumbnails = info.get("thumbnails", [])
        best_quality = (None, 0)
        for thumb in thumbnails:
            pixels_no = thumb.get("width", 0) * thumb.get("height", 0)
            if pixels_no >= best_quality[1]:
                best_quality = (thumb.get("url"), pixels_no)
        return best_quality[0]
