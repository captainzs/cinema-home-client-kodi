import xbmc
import xbmcgui
from lib import addon
from lib.models.types.media_sets import Collection, Similar
from lib.models.types.media_type import MediaType
from lib.services.client_service import ClientService
from lib.services.details_downloader import DetailsDownloaderTask
from lib.services.file_downloader import download_youtube
from lib.services.video_saver import VideoSaverThread
from lib.utils.logger import Logger
from lib.viewmodels.loading_dialog import LoadingDialog
from lib.viewmodels.seasons_dialog import SeasonsDialog
from lib.viewmodels.similars_dialog import SimilarsDialog
from lib.viewmodels.torrents_dialog import TorrentsDialog
from lib.viewmodels.videos_dialog import VideosDialog
from window import Window


class DetailsWindow(xbmcgui.WindowXML, Window):
    _logger = Logger.get_instance(__name__)

    XML_ID_LST_FAKE = 50
    XML_ID_BTN_DOWNLOAD = 81
    XML_ID_BTN_COLLECTION = 82
    XML_ID_BTN_SIMILARS = 83
    XML_ID_BTN_VIDEOS = 84
    XML_ID_BTN_FAVOR = 85
    XML_ID_BTN_REPORT = 86
    XML_ID_LST_SUBMENU = 190

    XML_ANIM_SAVER = "OnVideoSaver"
    XML_ANIM_READY = "OnMediaReady"
    XML_ANIM_SQUEEZE = "OnSqueeze"
    XML_ANIM_MINIMIZE = "OnMinimize"

    XML_OPENED_MENU = "OpenedMenuId"
    XML_SUB_LIST_SIZE = "SubListSize"

    @classmethod
    def get_instance(cls):
        return DetailsWindow('script-details_window.xml', addon.ADDON_PATH, 'default', '1080i', True,
                             player=xbmc.Player(),
                             client_service=ClientService.get_instance(),
                             loading_dialog=LoadingDialog.get_instance())

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXML.__init__(self, args[0], args[1], args[2], args[3], args[4])
        Window.__init__(self)
        self._player = kwargs["player"]
        self.__service = kwargs["client_service"]

        self.__media = None
        self._dynamic_data = None

        self._main_dialog = None
        self.__loader = kwargs["loading_dialog"]
        self._torrents_dialog = None
        self._seasons_dialog = None
        self._collections_dialog = None
        self._similars_dialog = None
        self._videos_dialog = None

        self._video_saver = None
        self._downloader = None
        return

    def doModalBrowser(self, dialog):
        self.__media = None
        self._main_dialog = dialog
        self.doModal()
        return

    def doModalWith(self, media):
        self.__media = media
        self._main_dialog = None
        self.doModal()
        return

    def onInit(self):
        if self.getFocusId() is not None:
            self.onClick(self.getFocusId())
        fake_lst = self.getControlList(DetailsWindow.XML_ID_LST_FAKE)
        if fake_lst.size() == 0:
            fake_item = xbmcgui.ListItem("Fake Init Item")
            fake_item.setProperty(DetailsWindow.XML_ANIM_READY, str(False))
            fake_item.setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(False))
            fake_item.setProperty(DetailsWindow.XML_ANIM_SQUEEZE, str(False))
            fake_lst.addItem(fake_item)
            if self._main_dialog is not None:
                self.await_main_dialog()
            elif self.__media is not None:
                self.update(self.__media)
        return

    def onAction(self, action):
        if self.is_video_saver_active():
            self._deactivate_video_saver()
            return
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            if self._main_dialog:
                self.await_main_dialog()
            else:
                self.close()
        return

    def onClick(self, control_id):
        if not self.is__media_ready():
            return
        if self.is_video_saver_active():
            self._deactivate_video_saver()
            return
        self.stop_update()
        try:
            if control_id == DetailsWindow.XML_ID_BTN_DOWNLOAD:
                if self.__media.get_type() == MediaType.MOVIE:
                    self._on_download_movie()
                elif self.__media.get_type() == MediaType.SHOW:
                    self._on_download_show()
            elif control_id == DetailsWindow.XML_ID_BTN_COLLECTION:
                self._on_collection()
            elif control_id == DetailsWindow.XML_ID_BTN_SIMILARS:
                self._on_similars()
            elif control_id == DetailsWindow.XML_ID_BTN_VIDEOS:
                self._on_videos()
            elif control_id == DetailsWindow.XML_ID_BTN_FAVOR:
                self._on_favor()
            elif control_id == DetailsWindow.XML_ID_BTN_REPORT:
                self._on_report()
        finally:
            self.clearProperty(DetailsWindow.XML_OPENED_MENU)
            self.clearProperty(DetailsWindow.XML_SUB_LIST_SIZE)
        return

    def _on_download_movie(self):
        if self._torrents_dialog is None:
            movie_w_torrents = self.__loader.load(10, self.__service.request_movie_torrents, self.__media.get_imdb_id())
            self._torrents_dialog = TorrentsDialog.get_instance(movie_w_torrents.get_torrents())
        self.setProperty(DetailsWindow.XML_SUB_LIST_SIZE, str(self._torrents_dialog.size()))
        selected = self._torrents_dialog.doModal()
        if selected is not None:
            self.__service.request_download_movie(selected.get_id())
        return

    def _on_download_show(self):
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(True))
        if self._seasons_dialog is None:
            show_w_torrents = self.__loader.load(10, self.__service.request_show_torrents, self.__media.get_imdb_id())
            self._seasons_dialog = SeasonsDialog.get_instance(show_w_torrents)
        self._seasons_dialog.doModal()
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(False))
        return

    def _on_collection(self):
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(True))
        if self._collections_dialog is None:
            collection = self.__media.get_collection()
            collections = []
            if collection is not None:
                if self.__media.get_type() == MediaType.MOVIE:
                    ms = Collection.of_movies(collection)
                else:
                    ms = Collection.of_shows(collection)
                collections = self.__loader.load(10, self.__service.request_lst, ms.get_path(1), ms.get_body(),
                                                 ms.get_media_type())
            self._collections_dialog = SimilarsDialog.get_instance(collections)
        self.setProperty(DetailsWindow.XML_SUB_LIST_SIZE, str(self._collections_dialog.size()))
        selected = self._collections_dialog.doModal()
        if selected is not None:
            sub_window = DetailsWindow.get_instance()
            sub_window.doModalWith(selected)
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(False))
        return

    def _on_similars(self):
        if self._similars_dialog is None:
            if self.__media.get_type() == MediaType.MOVIE:
                ms = Similar.to_movie(self.__media.get_title(), self.__media.get_tmdb_id())
            else:
                ms = Similar.to_show(self.__media.get_title(), self.__media.get_tmdb_id())
            similars = self.__loader.load(15, self.__service.request_lst, ms.get_path(1), ms.get_body(),
                                          ms.get_media_type())
            self._similars_dialog = SimilarsDialog.get_instance(similars)
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(True))
        self.setProperty(DetailsWindow.XML_SUB_LIST_SIZE, str(self._similars_dialog.size()))
        selected = self._similars_dialog.doModal()
        if selected is not None:
            sub_window = DetailsWindow.get_instance()
            sub_window.doModalWith(selected)
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(False))
        return

    def _on_videos(self):
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(True))
        if self._videos_dialog is None:
            videos = self.__media.get_videos()
            self._videos_dialog = VideosDialog.get_instance(videos)
        self.setProperty(DetailsWindow.XML_SUB_LIST_SIZE, str(self._videos_dialog.size()))
        video = self._videos_dialog.doModal()
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(False))
        if video is not None:
            if not video.is_available():
                path = download_youtube(video.get_url())
                video.set_path(path)
            if video.is_available():
                self._player.play(item=video.get_path(),
                                  listitem=self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE), windowed=False)
        return

    def _on_favor(self):
        is_favored = self._dynamic_data.is_favored()
        new_value = not eval(is_favored)
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty("IsFavored", str(new_value))
        return

    def _on_report(self):
        errors = [addon.ADDON.getLocalizedString(30013), addon.ADDON.getLocalizedString(30014),
                  addon.ADDON.getLocalizedString(30015), addon.ADDON.getLocalizedString(30016),
                  addon.ADDON.getLocalizedString(30017), addon.ADDON.getLocalizedString(30018),
                  addon.ADDON.getLocalizedString(30019) + u"..."]
        selected = xbmcgui.Dialog().select(addon.ADDON.getLocalizedString(30020), errors, 0, -1, False)
        if selected == len(errors) - 1:
            message = xbmcgui.Dialog().input(addon.ADDON.getLocalizedString(30021), "", xbmcgui.INPUT_ALPHANUM)
        else:
            message = errors[selected]
        self.__service.report(self.__media.get_imdb_id(), message)
        return

    def update(self, media):
        self.stop_update()
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_READY, str(False))
        if media is not None:
            self._downloader = DetailsDownloaderTask(self.__service)
            self._downloader.start_download(media, self._on_ready, self.start_video)
        self.__media = media
        self._dynamic_data = None
        self._torrents_dialog = None
        self._seasons_dialog = None
        self._collections_dialog = None
        self._similars_dialog = None
        self._videos_dialog = None
        return

    def stop_update(self):
        self.stop_video()
        if self._downloader:
            self._downloader.stop()
        return

    def _on_ready(self, detailed_item, dynamic_data):
        self.__media = detailed_item.get_media()
        self._dynamic_data = dynamic_data
        old_item = self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE)
        detailed_item.setProperty(DetailsWindow.XML_ANIM_READY, str(True))
        detailed_item.setProperty(DetailsWindow.XML_ANIM_MINIMIZE, str(False))
        detailed_item.setProperty(DetailsWindow.XML_ANIM_SQUEEZE, old_item.getProperty(DetailsWindow.XML_ANIM_SQUEEZE))
        detailed_item.setProperty("IsFavored", str(dynamic_data.is_favored()))
        self.getControlList(DetailsWindow.XML_ID_LST_FAKE).reset()
        self.getControlList(DetailsWindow.XML_ID_LST_FAKE).addItem(detailed_item)
        self.setFocusId(DetailsWindow.XML_ID_BTN_DOWNLOAD)
        return

    def is__media_ready(self):
        return self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).getProperty(DetailsWindow.XML_ANIM_READY) == str(
            True)

    def start_video(self, video):
        if not self._player.isPlaying() and video.is_available():
            self._video_saver = VideoSaverThread(self._activate_video_saver)
            self._video_saver.start()
            self._player.play(item=video.get_path(),
                              listitem=self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE), windowed=True)
        return

    def stop_video(self):
        if self._player.isPlaying():
            self._player.stop()
            if self._video_saver:
                self._video_saver.stop()
            self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_SAVER,
                                                                                str(False))
        return

    def _activate_video_saver(self):
        if not self.is_video_saver_active():
            self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_SAVER,
                                                                                str(True))
        return

    def _deactivate_video_saver(self):
        if self.is_video_saver_active():
            self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_SAVER,
                                                                                str(False))
            self._video_saver.restart()
        return

    def is_video_saver_active(self):
        return self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).getProperty(DetailsWindow.XML_ANIM_SAVER) == str(
            True)

    def await_main_dialog(self):
        if self._main_dialog is None:
            return
        self.stop_update()
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_SQUEEZE, str(True))
        self._main_dialog.doModalOver(self)
        self.getSelectedListItem(DetailsWindow.XML_ID_LST_FAKE).setProperty(DetailsWindow.XML_ANIM_SQUEEZE, str(False))
        self._deactivate_video_saver()
        return

    def close(self):
        try:
            self.stop_update()
            del self._downloader
            del self._video_saver
            if self._main_dialog:
                self._main_dialog.close()
                del self._main_dialog
            self.__loader.close()
            del self.__loader
            if self._torrents_dialog:
                self._torrents_dialog.close()
                del self._torrents_dialog
            if self._seasons_dialog:
                self._seasons_dialog.close()
                del self._seasons_dialog
            if self._collections_dialog:
                self._collections_dialog.close()
                del self._collections_dialog
            if self._similars_dialog:
                self._similars_dialog.close()
                del self._similars_dialog
            if self._videos_dialog:
                self._videos_dialog.close()
                del self._videos_dialog
        except Exception:
            self._logger.exception(u"Error happened when trying to finalize closure of details window!")
        finally:
            xbmcgui.Window.close(self)
