import xbmcgui
from control import Control
from lib.utils.logger import Logger
from lib.utils.override import override
from xbmcgui import ControlList


class Window(xbmcgui.Window):
    __logger = Logger.get_instance(__name__)

    def __init__(self):
        xbmcgui.Window.__init__(self)
        self.__fake_focus = xbmcgui.ControlButton(-50, -50, 0, 0, "")
        xbmcgui.Window.addControl(self, self.__fake_focus)
        self.__controls = []
        self.__focus_id = None
        self._opened = False
        return

    @override
    def onAction(self, action):
        focused = self.getControl(self.__focus_id)
        if isinstance(focused, Control):
            handled = focused.on_action(action)
            if handled is False and action.getId() == xbmcgui.ACTION_MOVE_UP:
                self.setFocus(focused.get_control_up())
            elif handled is False and action.getId() == xbmcgui.ACTION_MOVE_DOWN:
                self.setFocus(focused.get_control_down())
            elif handled is False and action.getId() == xbmcgui.ACTION_MOVE_LEFT:
                self.setFocus(focused.get_control_left())
            elif handled is False and action.getId() == xbmcgui.ACTION_MOVE_RIGHT:
                self.setFocus(focused.get_control_right())
        return

    @override
    def onFocus(self, control_id):
        if control_id == self.__fake_focus.getId():
            return
        old = self.getControl(self.__focus_id)
        if isinstance(old, Control):
            old.unfocus()
        new = self.getControl(control_id)
        if isinstance(new, Control):
            new.focus()
        self.__focus_id = control_id
        return

    @override
    def addControl(self, control):
        if control is None:
            return
        return self.addControls([control])

    @override
    def addControls(self, controls):
        xbmc_controls = []
        for control in controls:
            if isinstance(control, Control):
                self.__controls.append(control)
                sub_controls = control.attach(id(control), self)
                for sub_control in sub_controls:
                    if isinstance(sub_control, xbmcgui.Control):
                        xbmc_controls.append(sub_control)
            elif isinstance(control, xbmcgui.Control):
                xbmc_controls.append(control)
        xbmcgui.Window.addControls(self, xbmc_controls)
        return

    @override
    def getControl(self, control_id):
        # type: (int) -> Control
        found = None
        try:
            found = xbmcgui.Window.getControl(self, control_id)
        except Exception:
            for control in self.__controls:
                if control.getId() == control_id:
                    found = control
        return found

    @override
    def getFocus(self):
        try:
            found = xbmcgui.Window.getFocus(self)
        except RuntimeError:
            found = self.getControl(self.__focus_id)
        return found

    @override
    def getFocusId(self):
        return self.__focus_id

    @override
    def setFocus(self, control):
        if control is None:
            return
        return self.setFocusId(control.getId())

    @override
    def setFocusId(self, control_id):
        control = self.getControl(control_id)
        if control is None:
            return
        if isinstance(control, Control):
            xbmcgui.Window.setFocus(self, self.__fake_focus)
            self.onFocus(control_id)
        else:
            xbmcgui.Window.setFocusId(self, control_id)
        return

    @override
    def show(self):
        self._opened = True
        xbmcgui.Window.show(self)
        return

    @override
    def doModal(self):
        self._opened = True
        xbmcgui.Window.doModal(self)
        return

    @override
    def close(self):
        self._opened = False
        xbmcgui.Window.close(self)
        return

    def is_opened(self):
        return self._opened is True

    def is_closed(self):
        return self._opened is False

    def getControlList(self, xml_id_lst):
        return self.getControl(xml_id_lst)  # type: ControlList

    def getSelectedListItem(self, xml_id_lst):
        lst = self.getControlList(xml_id_lst)  # type: ControlList
        return lst.getSelectedItem()
