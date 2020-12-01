import os

import xbmc
import xbmcaddon

ADDON = xbmcaddon.Addon()
ADDON_PATH = xbmc.translatePath(ADDON.getAddonInfo('path'))
ADDON_DATA_PATH = xbmc.translatePath(ADDON.getAddonInfo('profile'))
ADDON_IMAGES_PATH = os.path.join(ADDON_DATA_PATH, "images")
ADDON_VIDEOS_PATH = os.path.join(ADDON_DATA_PATH, "videos")
