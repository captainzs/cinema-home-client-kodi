import threading
import time

from lib.utils.stoppable_thread import StoppableThread


class VideoSaverThread(StoppableThread):
    def __init__(self, callback):
        StoppableThread.__init__(self)
        self._callback = callback
        self._restart_event = threading.Event()
        return

    def run(self):
        self._restart_event.clear()
        while not self.stopped():
            if not self._restart_event.is_set():
                self._callback()
            self._restart_event.clear()
            self._wait_until_restart_or(5)
        return

    def restart(self):
        self._restart_event.set()

    def _wait_until_restart_or(self, secs):
        start = time.time()
        while (time.time() - start < secs) and not self._restart_event.is_set():
            time.sleep(0.01)
            pass
        return
