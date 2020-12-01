import time

import xbmc
from lib.utils.logger import Logger
from lib.utils.stoppable_thread import StoppableThread


class GroupedAnimationThread(StoppableThread):
    __logger = Logger.get_instance(__name__)

    def __init__(self, duration):
        StoppableThread.__init__(self)
        self.__elements = []
        self.__duration = duration
        return

    def size(self):
        return len(self.__elements)

    def add(self, control_fix, control_animator, animations):
        if not self.is_alive():
            self.__elements.append((control_fix, control_animator, animations))
        return

    def run(self):
        trigger = "OnGroupedAnimation-{}".format(id(self))
        condition = "String.IsEqual(Window.Property({}),True)".format(trigger)

        for element in self.__elements:
            animations = []
            for anim in element[2]:
                animations.extend(anim.to_list(self.__duration, condition))
            element[1].setAnimations(animations)
            element[1].setVisible(True)

        xbmc.executebuiltin('SetProperty({},True)'.format(trigger))

        time_secs = self.__duration / 1000.0
        start = time.time()
        while time.time() - start < time_secs and not self.stopped():
            time.sleep(0.01)
            pass

        for element in self.__elements:
            for animation in element[2]:
                animation.persist(element[0])
            element[0].setVisible(True)
            element[1].render(None)
            element[1].setAnimations([])
        xbmc.executebuiltin('ClearProperty({})'.format(trigger))

        del self.__elements[:]
        self.stop()
        return
