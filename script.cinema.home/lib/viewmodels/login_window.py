import random
import threading

import xbmcgui
from lib import addon
from lib.models.types.genres import Genre
from lib.models.types.media_sets import Recommended, Popular, Categorized, Newest, Best, Streamed
from lib.models.types.networks import Network
from lib.services.client_service import ClientService
from lib.utils.logger import Logger
from lib.utils.override import override
from lib.viewmodels.details_window import DetailsWindow
from lib.viewmodels.main_dialog import MainDialog
from window import Window


class LogInWindow(xbmcgui.WindowXML, Window):
    _logger = Logger.get_instance(__name__)

    @classmethod
    def get_instance(cls):
        return LogInWindow('script-login_window.xml', addon.ADDON_PATH, 'default', '1080i', True,
                           client_service=ClientService.get_instance())

    def __init__(self, *args, **kwargs):
        xbmcgui.WindowXML.__init__(self, args[0], args[1], args[2], args[3], args[4])
        Window.__init__(self)
        self.__service = kwargs['client_service']
        self.__threads = None
        return

    def onInit(self):
        if self.__threads is None:
            movie_groups, show_groups = self.__media_sets()
            self.__threads = self.__load(movie_groups, show_groups)
            dialog = MainDialog.get_instance()
            dialog.set_up(movie_groups, show_groups, MainDialog.XML_ID_MENU_MOVIES)
            window = DetailsWindow.get_instance()
            window.doModalBrowser(dialog)
            self.close()
        return

    def onAction(self, action):
        if action.getId() == xbmcgui.ACTION_PREVIOUS_MENU or action.getId() == xbmcgui.ACTION_NAV_BACK:
            self.close()
        return

    @staticmethod
    def __media_sets():
        main_genres = [Genre.ACTION, Genre.ANIMATION, Genre.COMEDY, Genre.CRIME, Genre.DOCUMENTARY, Genre.DRAMA,
                       Genre.ROMANCE, Genre.SCI_FI, Genre.THRILLER, Genre.HORROR, Genre.WAR]
        random.shuffle(main_genres)
        movie_groups = [Popular.movies(),
                        Categorized.movies_by_genre(main_genres[0]),
                        Recommended.movies_by_staff(),
                        Categorized.movies_by_genre(main_genres[1]),
                        Newest.movies(),
                        Categorized.movies_by_genre(main_genres[2]),
                        Streamed.movies_of(Network.NETFLIX),
                        Categorized.movies_by_genre(main_genres[3]),
                        Best.movies(),
                        Categorized.movies_by_genre(main_genres[4]),
                        Categorized.movies_by_genre(main_genres[5]),
                        Categorized.movies_by_genre(main_genres[6]),
                        Categorized.movies_by_genre(main_genres[7]),
                        Categorized.movies_by_genre(main_genres[8]),
                        Categorized.movies_by_genre(main_genres[9]),
                        Categorized.movies_by_genre(main_genres[10])]
        show_groups = [Popular.shows(),
                       Categorized.shows_by_genre(main_genres[0]),
                       Recommended.shows_by_staff(),
                       Categorized.shows_by_genre(main_genres[1]),
                       Newest.shows(),
                       Categorized.shows_by_genre(main_genres[2]),
                       Streamed.shows_of(Network.NETFLIX),
                       Categorized.shows_by_genre(main_genres[3]),
                       Best.shows(),
                       Categorized.shows_by_genre(main_genres[4]),
                       Categorized.shows_by_genre(main_genres[5]),
                       Categorized.shows_by_genre(main_genres[6]),
                       Categorized.shows_by_genre(main_genres[7]),
                       Categorized.shows_by_genre(main_genres[8]),
                       Categorized.shows_by_genre(main_genres[9]),
                       Categorized.shows_by_genre(main_genres[10])]
        return movie_groups, show_groups

    def __load(self, priority_groups, non_priority_groups):
        threads = []
        for task in priority_groups:
            thread = threading.Thread(target=self._load_media_set, args=(task,))
            threads.append(thread)
            thread.start()
        for t in threads:
            t.join()
        for task in non_priority_groups:
            thread = threading.Thread(target=self._load_media_set, args=(task,))
            threads.append(thread)
            thread.start()
        return threads

    def _load_media_set(self, mset):
        lst = self.__service.request_lst(mset.get_path(1), mset.get_body(), mset.get_media_type())
        mset.extend(1, lst)
        return

    @override
    def close(self):
        Window.close(self)
        for t in self.__threads:
            t.join()
        return
