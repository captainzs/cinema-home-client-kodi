import math
import time

import definitions
import xbmcgui
from animation_thread import GroupedAnimationThread
from animations import SlideAnimation, FadeAnimation
from control_group import ControlGroup
from definitions import Orientation, Vector, ScrollStop
from lib.utils.logger import Logger
from lib.utils.override import override
from rect import intersects, Rect, join, center, contains


class ControlList(ControlGroup):
    __logger = Logger.get_instance(__name__)
    _KODI_RENDER_SECS = 0.001

    def __init__(self, x, y, width, height, orientation=Orientation.HORIZONTAL,
                 scroller=None, scroll_stop=None, scroll_time=200,
                 layout=None, padding_left=0, padding_top=0):
        ControlGroup.__init__(self, x, y, width, height, self._init_controls(width, height, orientation, layout))
        self.__orientation = orientation
        self.__scroller = scroller
        self.__scroll_stop = scroll_stop
        self.__scroll_time = scroll_time
        self._layout = layout
        self._padding_left = padding_left
        self._padding_top = padding_top

        self.__selected = None
        self.__scroll_position = Vector(0, 0)

        self.__items = []
        self.__animation_t = None
        return

    @staticmethod
    def _init_controls(width, height, orientation, layout):
        controls = []
        if layout is not None:
            if orientation == Orientation.VERTICAL:
                has_space_for = int(math.ceil(float(height) / layout.height()))
            else:
                has_space_for = int(math.ceil(float(width) / layout.width()))
            can_animate_concurrently = has_space_for + 2
            needed_for_animations = can_animate_concurrently * 2
            for i in range(0, needed_for_animations):
                controls.append(layout.new())
        return controls

    def init_state(self, selected, scroll_position):
        if len(self.__items) > 0:
            raise RuntimeError("Can not set state of list after items added!")
        self.__selected = selected
        self.__scroll_position = scroll_position
        return

    @override
    def on_action(self, action):
        if self.__selected is not None and len(self.__items) > self.__selected:
            control = self.__find_control(self.__items[self.__selected])
            if control:
                self.wait_for_scroll(False)
                if control.on_action(action) is True:
                    return True

        action_id = action.getId()
        action_code = action.getButtonCode()
        if action_id == xbmcgui.ACTION_MOVE_DOWN and action_code == definitions.GUI_KEY_DOWN_PRESS_CODE:
            return self.move_down()
        elif action_id == xbmcgui.ACTION_MOVE_UP and action_code == definitions.GUI_KEY_UP_PRESS_CODE:
            return self.move_up()
        elif action_id == xbmcgui.ACTION_MOVE_LEFT and action_code == definitions.GUI_KEY_LEFT_PRESS_CODE:
            return self.move_left()
        elif action_id == xbmcgui.ACTION_MOVE_RIGHT and action_code == definitions.GUI_KEY_RIGHT_PRESS_CODE:
            return self.move_right()
        return False

    @override
    def focus(self):
        if self.__selected is None:
            return
        self.__find_control(self.__items[self.__selected]).focus()
        return

    @override
    def unfocus(self):
        if self.__selected is None:
            return
        self.__find_control(self.__items[self.__selected]).unfocus()
        return

    def size(self):
        return len(self.__items)

    def get_orientation(self):
        return self.__orientation

    def getSelectedPosition(self):
        return self.__selected

    def getSelectedItem(self):
        if self.__selected is None:
            return None
        return self.__items[self.__selected]

    def get_scroll_position(self):
        return self.__scroll_position

    def reset(self):
        for i in range(0, len(self._controls)):
            self._controls[i].render(None)
        del self.__items[:]
        self.__selected = None
        self.__scroll_position = Vector(0, 0)
        self.wait_for_scroll(True)
        return

    def addItem(self, item):
        if item is None:
            return
        return self.addItems([item])

    def addItems(self, items):
        if items is None:
            return

        self.wait_for_scroll(False)

        for item in items:
            next_index = len(self.__items)
            self.__items.append(item)
            if self.__selected is None:
                self.__selected = next_index
            to_rect = self.__item_bounds(item)
            if intersects(to_rect, self.bounds()):
                control = self.__find_control(None)
                self.__render_item(control, item)
        return

    def move_up(self):
        if self.__orientation == Orientation.HORIZONTAL:
            return False
        return self.selectItem(self.__selected - 1)

    def move_down(self):
        if self.__orientation == Orientation.HORIZONTAL:
            return False
        return self.selectItem(self.__selected + 1)

    def move_left(self):
        if self.__orientation == Orientation.VERTICAL:
            return False
        return self.selectItem(self.__selected - 1)

    def move_right(self):
        if self.__orientation == Orientation.VERTICAL:
            return False
        return self.selectItem(self.__selected + 1)

    def selectItem(self, index):
        if index is None or index < 0 or index >= len(self.__items):
            return False
        if self.__selected == index:
            return False
        from_item = self.__items[self.__selected]
        to_item = self.__items[index]

        self.__selected = index
        self.__scroll_selection(from_item, to_item)
        return True

    def __scroll_selection(self, from_item, to_item):
        if self.__scroller is None:
            return
        vector = self.__scroller.direction_vector(center(self.__item_bounds(from_item)),
                                                  center(self.__item_bounds(to_item)))
        vector = self.__scroll_normalization(vector)
        vector = Vector(0, vector.y) if self.__orientation == Orientation.VERTICAL else Vector(vector.x, 0)
        scrolled = self.__scroll(vector.x, vector.y)
        if scrolled is False:
            self.__find_control(from_item).unfocus()
            self.__find_control(to_item).focus()
        return

    def __scroll_normalization(self, scroll_vector):
        if self.__scroll_stop is None:
            return scroll_vector
        delta_x = scroll_vector.x
        delta_y = scroll_vector.y
        if scroll_vector.y > 0:
            hanging = max(0, self.__items_bottom_right_vector().y - self.getY() - self.getHeight())
            if self.__scroll_stop == ScrollStop.EDGE:
                delta_y = min(hanging, scroll_vector.y)
            elif self.__scroll_stop == ScrollStop.LAST:
                hang_count = int(math.ceil(float(hanging) / self._layout.height()))
                delta_y = min(scroll_vector.y, hang_count * self._layout.height()) if hanging > 0 else 0
        elif scroll_vector.y < 0:
            hanging = max(0, self.__scroll_position.y)
            if self.__scroll_stop == ScrollStop.EDGE:
                delta_y = max(-hanging, scroll_vector.y)
            elif self.__scroll_stop == ScrollStop.LAST:
                hang_count = int(math.ceil(float(hanging) / self._layout.height()))
                delta_y = max(scroll_vector.y, -(hang_count * self._layout.height())) if hanging > 0 else 0
        if scroll_vector.x > 0:
            hanging = max(0, self.__items_bottom_right_vector().x - self.getX() - self.getWidth())
            if self.__scroll_stop == ScrollStop.EDGE:
                delta_x = min(hanging, scroll_vector.x)
            elif self.__scroll_stop == ScrollStop.LAST:
                hang_count = int(math.ceil(float(hanging) / self._layout.width()))
                delta_x = min(scroll_vector.x, hang_count * self._layout.width()) if hanging > 0 else 0
        elif scroll_vector.x < 0:
            hanging = max(0, self.__scroll_position.x)
            if self.__scroll_stop == ScrollStop.EDGE:
                delta_x = max(-hanging, scroll_vector.x)
            elif self.__scroll_stop == ScrollStop.LAST:
                hang_count = int(math.ceil(float(hanging) / self._layout.width()))
                delta_x = max(scroll_vector.x, -(hang_count * self._layout.width())) if hanging > 0 else 0
        return Vector(delta_x, delta_y)

    def __scroll(self, delta_x, delta_y):
        if delta_x == 0 and delta_y == 0:
            return False

        self.wait_for_scroll(False)
        self.__animation_t = GroupedAnimationThread(self.__scroll_time)

        slide_x = -delta_x
        slide_y = -delta_y
        slide_animation = SlideAnimation(slide_x, slide_y)

        animations_2_items = {}
        for item in self.__items:
            from_rect = self.__item_bounds(item)
            to_rect = Rect(from_rect.x + slide_x, from_rect.y + slide_y, from_rect.width, from_rect.height)
            movement_rect = join(from_rect, to_rect)
            if intersects(self.bounds(), movement_rect):
                animations = [slide_animation]
                from_value = self.__item_opacity(from_rect)
                to_value = self.__item_opacity(to_rect)
                if from_value != to_value:
                    animations.append(FadeAnimation(from_value, to_value))
                animations_2_items[item] = animations

        half_controls_count = int(len(self._controls) / 2)
        for c in range(0, half_controls_count):
            control_fix = self._controls[c]
            current_item = control_fix.get_item()
            if current_item in animations_2_items:
                control_animator = self._controls[c + half_controls_count]
                self.__render_item(control_animator, current_item)
                time.sleep(ControlList._KODI_RENDER_SECS)
                self.__render_item(control_fix, current_item, False)
                self.__animation_t.add(control_fix, control_animator, animations_2_items[current_item])
                del animations_2_items[current_item]
            else:
                self._controls[c].render(None)
                self._controls[c + half_controls_count].render(None)

        for item, animations in animations_2_items.items():
            control_fix = self.__find_control(None)
            control_animator = self.__find_control(None, is_animator=True)
            self.__render_item(control_animator, item)
            time.sleep(ControlList._KODI_RENDER_SECS)
            self.__render_item(control_fix, item, False)
            self.__animation_t.add(control_fix, control_animator, animations)

        if self.__animation_t.size() > 0:
            self.__animation_t.start()
        self.__scroll_position = Vector(self.__scroll_position.x + delta_x, self.__scroll_position.y + delta_y)
        return True

    def __items_bottom_right_vector(self):
        if self.__orientation == Orientation.VERTICAL:
            return Vector(self.getX() - self.__scroll_position.x + self._padding_left + self._layout.width(),
                          self.getY() - self.__scroll_position.y + self._padding_top +
                          (self._layout.height() * self.size()))
        return Vector(
            self.getX() - self.__scroll_position.x + self._padding_left + (self._layout.width() * self.size()),
            self.getY() - self.__scroll_position.y + self._padding_top + self._layout.height())

    def __render_item(self, to_control, item, visible=True):
        index = self.__items.index(item)
        bounds = self.__item_bounds(item)
        to_control.setVisible(visible)
        to_control.set_opacity(self.__item_opacity(bounds))
        to_control.setPosition(bounds.x, bounds.y)
        to_control.render(item)
        to_control.focus() if self.__selected == index else to_control.unfocus()
        return

    def __find_control(self, with_item, is_animator=False):
        found = None
        for control in self.__get_controls(is_animator):
            if control.get_item() == with_item:
                found = control
                break
        return found

    def __get_controls(self, is_animator):
        half_count = int(len(self._controls) / 2.0)
        if is_animator:
            return self._controls[half_count::]
        return self._controls[0:half_count]

    def __item_opacity(self, bounds):
        containing = contains(self.bounds(), bounds)
        outside = not intersects(self.bounds(), bounds)
        return 100 if containing else 0 if outside else 50

    def __item_bounds(self, item):
        index = self.__items.index(item)
        position = self._item_position(index)
        return Rect(position.x, position.y, self._layout.width(), self._layout.height())

    def _item_position(self, item_index):
        is_horizontal = int(self.__orientation == Orientation.HORIZONTAL)
        is_vertical = int(self.__orientation == Orientation.VERTICAL)
        return Vector(self.getX() - self.__scroll_position.x + self._padding_left +
                      (self._layout.width() * item_index * is_horizontal),
                      self.getY() - self.__scroll_position.y + self._padding_top +
                      (self._layout.height() * item_index * is_vertical))

    def wait_for_scroll(self, wait):
        if self.__animation_t is None:
            return
        if wait is False and not self.__animation_t.stopped():
            self.__animation_t.stop()
        if self.__animation_t.is_alive():
            self.__animation_t.join()
        self.__animation_t = None
        return
