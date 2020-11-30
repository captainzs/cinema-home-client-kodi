import time

from lib.services.file_downloader import download_youtube
from lib.utils.stoppable_thread import StoppableThread


class DetailsDownloaderTask(StoppableThread):
    def __init__(self, client_service):
        StoppableThread.__init__(self)
        self._client_service = client_service
        self._media = None
        self._on_ready = None
        self._on_video_ready = None
        return

    def start_download(self, media, on_ready, on_video_ready):
        self._media = media
        self._on_ready = on_ready
        self._on_video_ready = on_video_ready
        StoppableThread.start(self)
        return

    def run(self):
        start = time.time()

        detailed_media = self._client_service.request_details(self._media.get_imdb_id(), self._media.get_type())
        if self.stopped():
            return
        dynamic_data = self._client_service.request_dynamic_data(detailed_media.get_imdb_id())

        while time.time() - start < 0.3:
            pass
        if self.stopped():
            return

        item = detailed_media.to_list_item()
        if self.stopped():
            return

        self._on_ready(item, dynamic_data)

        videos = detailed_media.get_videos()
        downloaded_video = self.__download_one_video(videos)
        if downloaded_video is not None:
            while time.time() - start < 10.0:
                pass
            if self.stopped():
                return
            self._on_video_ready(downloaded_video)
        self.stop()
        return

    def __download_one_video(self, videos):
        if videos is not None:
            for video in videos:
                if self.stopped():
                    return None
                try:
                    path = download_youtube(video.get_url())
                    video.set_path(path)
                    return video
                except Exception:
                    pass
        return None
