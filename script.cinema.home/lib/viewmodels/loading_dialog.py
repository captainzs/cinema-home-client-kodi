import math
import multiprocessing
import multiprocessing.pool as mpp
import os
import threading
import time
from contextlib import closing

import xbmcgui
from lib import addon
from lib.utils.logger import Logger
from window import Window


class LoadingDialog(xbmcgui.WindowXMLDialog, Window):
    _logger = Logger.get_instance(__name__)

    CIRCLES_COUNT = 8
    CIRCLES_RADIUS = 25
    ANIM_RADIUS = 150
    ANIM_DELAY_SECS = 0.2
    ANIM_TIME_MILISECS = ANIM_DELAY_SECS * 8 * 1000

    @classmethod
    def get_instance(cls):
        return LoadingDialog('script-loading_dialog.xml', addon.ADDON_PATH, 'default', '1080i')

    def __init__(self, *args, **kwargs):
        Window.__init__(self)
        xbmcgui.WindowXMLDialog.__init__(self, args[0], args[1], args[2], args[3])
        self._init_shadow()
        self._init_bubbles()
        self._thread = None
        return

    def _init_shadow(self):
        white_img_path = os.path.join(addon.ADDON_PATH, "resources", "media", "white.bmp")
        shadow = xbmcgui.ControlImage(0, 0, xbmcgui.getScreenWidth(), xbmcgui.getScreenHeight(),
                                      white_img_path, 0, "FF000000")
        self.addControl(shadow)
        shadow.setAnimations([
            ('WindowOpen', 'effect=fade start=0 end=80 time=200',),
            ('WindowClose', 'effect=fade start=80 end=0 time=200',)
        ])
        return

    def _init_bubbles(self):
        center_x = xbmcgui.getScreenWidth() / 2.0
        center_y = xbmcgui.getScreenHeight() / 2.0
        controls = []
        current_x, current_y = LoadingDialog.ANIM_RADIUS, 0
        for i in range(0, LoadingDialog.CIRCLES_COUNT):
            controls.append(self._add_circle_control(center_x + current_x, center_y + current_y, i))
            current_x, current_y = self._rotate_45_counterclockwise(current_x, current_y)
        return

    def _add_circle_control(self, x, y, order_index):
        circle_img_path = os.path.join(addon.ADDON_PATH, "resources", "media", "circle.png")
        control = xbmcgui.ControlImage(int(x - LoadingDialog.CIRCLES_RADIUS), int(y - LoadingDialog.CIRCLES_RADIUS),
                                       int(LoadingDialog.CIRCLES_RADIUS * 2), int(LoadingDialog.CIRCLES_RADIUS * 2),
                                       circle_img_path, 0, "00CBE354")
        condition_str = "String.IsEqual(Window.Property(LoadingStart{}),True)".format(order_index)
        self.addControl(control)
        control.setVisibleCondition('{}'.format(condition_str))
        control.setColorDiffuse('FFCBE354')
        control.setAnimations([
            ('conditional', 'effect=fade start=100 end=0 time={} condition={} loop=true'
             .format(LoadingDialog.ANIM_TIME_MILISECS, condition_str),),
            ('conditional', 'effect=zoom center=auto start=100,100 end=0,0 time={} condition={} loop=true'
             .format(LoadingDialog.ANIM_TIME_MILISECS, condition_str),),
            ('WindowClose', 'effect=fade end=0 time=200',)
        ])
        return control

    def show(self):
        if self.is_opened():
            return
        Window.show(self)
        self._thread = threading.Thread(target=self._start, args=())
        self._thread.start()
        return

    def load(self, timeout_secs, function, *args):
        return_val = None
        try:
            self.show()
            try_again = True
            while try_again:
                try_again = False
                try:
                    with closing(mpp.ThreadPool(processes=1)) as pool:
                        async_result = pool.apply_async(func=function, args=args)
                        return_val = async_result.get(timeout_secs)
                except multiprocessing.TimeoutError:
                    try_again = xbmcgui.Dialog().yesno(heading=addon.ADDON.getLocalizedString(30022),
                                                       line1=addon.ADDON.getLocalizedString(30023),
                                                       nolabel=addon.ADDON.getLocalizedString(30024),
                                                       yeslabel=addon.ADDON.getLocalizedString(30025))
        finally:
            self.close()
        return return_val

    def _start(self):
        time.sleep(LoadingDialog.ANIM_DELAY_SECS)
        for i in range(0, LoadingDialog.CIRCLES_COUNT):
            if self.is_closed():
                break
            self.setProperty("LoadingStart{}".format(i), str(True))
            time.sleep(LoadingDialog.ANIM_DELAY_SECS)
        return

    def close(self):
        Window.close(self)
        if self._thread is not None:
            self._thread.join()
        for i in range(0, LoadingDialog.CIRCLES_COUNT):
            self.clearProperty("LoadingStart{}".format(i))
        return

    @staticmethod
    def _rotate_45_counterclockwise(x, y):
        in_radians = math.radians(45)
        new_x = (x * math.cos(in_radians)) - (y * math.sin(in_radians))
        new_y = (x * math.sin(in_radians)) + (y * math.cos(in_radians))
        return new_x, new_y
