from collections import namedtuple

GUI_KEY_UP_PRESS_CODE = 61568
GUI_KEY_DOWN_PRESS_CODE = 61569
GUI_KEY_LEFT_PRESS_CODE = 61570
GUI_KEY_RIGHT_PRESS_CODE = 61571

Position = namedtuple('Position', 'column row')
Scope = namedtuple('Scope', 'columns rows')
Alignment = namedtuple('Alignment', 'size scope')
Vector = namedtuple('Vector', 'x y')
Rect = namedtuple('Rect', 'x y width height')


class Orientation:
    HORIZONTAL = 0
    VERTICAL = 1


class ScrollStop:
    EDGE = 0
    LAST = 1
