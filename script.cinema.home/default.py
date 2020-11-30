import os

from lib import addon

# The directory for addon data/images is not created automatically
# We have to call it before any kind of import
if not os.path.exists(addon.ADDON_DATA_PATH):
    os.mkdir(addon.ADDON_DATA_PATH)
if not os.path.exists(addon.ADDON_IMAGES_PATH):
    os.mkdir(addon.ADDON_IMAGES_PATH)
if not os.path.exists(addon.ADDON_VIDEOS_PATH):
    os.mkdir(addon.ADDON_VIDEOS_PATH)

from lib.main import Main


def main():
    Main().run()
    return


if __name__ == "__main__":
    main()
