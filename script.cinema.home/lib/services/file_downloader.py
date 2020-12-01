import base64
import os

import requests

from lib import addon
from lib.utils.logger import Logger
from ydl_wrapper import YoutubeDLWrapper

__logger = Logger.get_instance(__name__)


def try_download_one(downloadable_lst):
    if downloadable_lst is not None:
        for downloadable in downloadable_lst:
            url = downloadable.get_url()
            path = os.path.join(addon.ADDON_IMAGES_PATH, "{}.jpg".format(base64.urlsafe_b64encode(url)))
            try:
                download(url, path)
                downloadable.set_path(path)
                return downloadable
            except Exception:
                pass
    return None


def try_download_thumb(youtube_url):
    if youtube_url is None:
        return None
    # TODO return the url that youtube defines
    path = os.path.join(addon.ADDON_IMAGES_PATH, "{}".format(base64.urlsafe_b64encode(youtube_url)))
    if os.path.isfile(path):
        return path
    with YoutubeDLWrapper({}) as ydl:
        url = ydl.get_thumb_url(youtube_url)
        download(url, path)
    return path


def download(url, path):
    if url is None or path is None or os.path.isfile(path):
        return
    with requests.session() as session:
        response = session.get(url, timeout=5, allow_redirects=False)
        if response.status_code != 200:
            raise RuntimeError("Failed to download file from {}".format(url))
        with open(path, "wb") as file_:
            file_.write(response.content)
    return


# TODO attach cookie setting for age restricted videos
def download_youtube(url):
    if url is None:
        return None
    path = os.path.join(addon.ADDON_VIDEOS_PATH, "{}.mp4".format(base64.urlsafe_b64encode(url)))
    if os.path.isfile(path):
        return path
    # TODO not necessarily the best format needed
    # TODO attach cinema.home.logger with youtube-wrapper
    ydl_opts = {
        'outtmpl': path,
        'format': 'best'
        # 'logger': self._logger
    }
    with YoutubeDLWrapper(ydl_opts) as ydl:
        ydl.download([url])
    return path
