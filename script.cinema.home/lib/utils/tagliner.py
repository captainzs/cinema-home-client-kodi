import datetime
import locale

import xbmc
from lib import addon


def to_tagline(next_episode):
    if next_episode is None:
        return None
    date = next_episode.get_air_date()
    if date is None:
        return None
    episode_no = next_episode.get_episode_number()
    if episode_no < 2:
        tagline = addon.ADDON.getLocalizedString(30002)
    else:
        tagline = addon.ADDON.getLocalizedString(30001)
    if datetime.datetime.today().year == date.year:
        locale.setlocale(locale.LC_TIME, xbmc.getLanguage(xbmc.ISO_639_1) + ".utf8")
        tagline = u"{}: {} {}".format(tagline, date.strftime("%B"), date.day)
    else:
        tagline = u"{}: {}".format(tagline, date)
    return tagline
