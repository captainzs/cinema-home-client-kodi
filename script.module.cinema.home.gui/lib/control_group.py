import xbmcgui
from animations import FadeAnimation, has_effect, find_all
from control import Control
from lib.utils.logger import Logger
from lib.utils.override import override


class ControlGroup(Control):
    __logger = Logger.get_instance(__name__)

    def __init__(self, x, y, width, height, controls=None):
        Control.__init__(self, x, y, width, height)
        self._controls = controls if controls else []
        self.__opacity = None
        return

    @override
    def on_action(self, action):
        return False

    @override
    def focus(self):
        return

    @override
    def unfocus(self):
        return

    @override
    def attach(self, assigned_id, parent):
        tree = []
        Control.attach(self, assigned_id, parent)
        for control in self._controls:
            if isinstance(control, Control):
                sub_controls = control.attach(id(control), self)
                tree.extend(sub_controls)
        tree.extend(self._controls)
        return tree

    @override
    def setPosition(self, x, y):
        delta_x = x - self.getX()
        delta_y = y - self.getY()
        Control.setPosition(self, x, y)
        for control in self._controls:
            control.setPosition(control.getX() + delta_x, control.getY() + delta_y)
        return

    @override
    def setAnimations(self, animations):
        new_animations_w_fade = []
        new_animations_w_fade.extend(animations)
        if self.__opacity is not None and not has_effect("fade", animations):
            new_animations_w_fade.insert(0, FadeAnimation.to_tuple(self.__opacity, self.__opacity))
        Control.setAnimations(self, new_animations_w_fade)
        self.refresh_animations()
        return

    def get_cumulated_animations(self):
        parent = self.get_parent()
        if parent is None:
            return []
        if not isinstance(parent, ControlGroup):
            return self.get_animations()

        result = []
        parent_animations = parent.get_cumulated_animations()
        own_animations = self.get_animations()
        result.extend(parent_animations)
        result.extend(own_animations)

        parent_fades = find_all("fade", parent_animations)
        own_fades = find_all("fade", own_animations)
        fades = {}
        for parent_fade in parent_fades:
            if "condition=true" in parent_fade[1]:
                fades[parent_fade] = 1
            else:
                fades[parent_fade] = 4
        for own_fade in own_fades:
            if "condition=true" in own_fade[1]:
                fades[own_fade] = 2
            else:
                fades[own_fade] = 3
        priority_fade_max_value = max(fades.values())
        priority_fades = map(lambda y: y[0], filter(lambda x: x[1] == priority_fade_max_value, fades.items()))

        if len(fades) > 0:
            for anim in fades:
                result.remove(anim)
            result.extend(priority_fades)
        return result

    def refresh_animations(self):
        shall_be_animations = self.get_cumulated_animations()
        for control in self._controls:
            if isinstance(control, ControlGroup):
                control.refresh_animations()
            elif isinstance(control, xbmcgui.Control):
                control.setAnimations(shall_be_animations)
        return

    @override
    def setVisible(self, visible):
        if self.isVisible() == visible:
            return
        Control.setVisible(self, visible)
        self.refresh_visibility()
        return

    def refresh_visibility(self):
        shall_be_visible = self.get_visibility()
        for control in self._controls:
            if isinstance(control, ControlGroup):
                control.refresh_visibility()
            elif isinstance(control, xbmcgui.Control):
                control.setVisible(shall_be_visible)
        return

    def set_opacity(self, opacity):
        if self.__opacity == opacity:
            return
        self.__opacity = opacity
        self.refresh_opacity()
        if opacity == 0:
            self.setVisible(False)
        return

    def get_cumulated_opacity(self):
        parent = self.get_parent()
        if parent is None:
            return 0
        if not isinstance(parent, ControlGroup):
            return 100
        parent_opacity = parent.get_cumulated_opacity()
        return min(parent_opacity, self.__opacity if self.__opacity is not None else 100)

    def refresh_opacity(self):
        shall_be_opacity = self.get_cumulated_opacity()
        animations = self.get_animations()
        fades = find_all("fade", animations)
        for fade in fades:
            animations.remove(fade)
        animations.append(FadeAnimation.to_tuple(shall_be_opacity, shall_be_opacity))
        Control.setAnimations(self, animations)

        for control in self._controls:
            if isinstance(control, ControlGroup):
                control.refresh_opacity()
            elif isinstance(control, xbmcgui.Control):
                control.setAnimations(animations)
        return

    def __str__(self):
        return "ControlGroup - id:{} parent:{} bounds:{} visible:{} opacity:{} animations:{}".format(
            self.getId(), id(self.get_parent()), self.bounds(), self.isVisible(), self.__opacity, self.get_animations())
