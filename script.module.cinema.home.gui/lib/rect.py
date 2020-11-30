from definitions import Rect, Vector


def contains(rect1, rect2):
    # type: (Rect, Rect) -> bool
    l1 = Vector(rect1.x, rect1.y)
    r1 = Vector(rect1.x + rect1.width, rect1.y + rect1.height)
    l2 = Vector(rect2.x, rect2.y)
    r2 = Vector(rect2.x + rect2.width, rect2.y + rect2.height)
    if l2.x >= l1.x and r2.x <= r1.x and l2.y >= l1.y and r2.y <= r1.y:
        return True
    return False


def intersects(rect1, rect2):
    # type: (Rect, Rect) -> bool
    l1 = Vector(rect1.x, rect1.y)
    r1 = Vector(rect1.x + rect1.width, rect1.y + rect1.height)
    l2 = Vector(rect2.x, rect2.y)
    r2 = Vector(rect2.x + rect2.width, rect2.y + rect2.height)
    if l1.x >= r2.x or l2.x >= r1.x:
        return False
    if l1.y >= r2.y or l2.y >= r1.y:
        return False
    return True


def center(rect):
    # type: (Rect) -> Vector
    return Vector(rect.x + (rect.width / 2.0), rect.y + (rect.height / 2.0))


def join(rect1, rect2):
    # type: (Rect, Rect) -> Rect
    min_x = min(rect1.x, rect2.x)
    min_y = min(rect1.y, rect2.y)
    max_x = max(rect1.x + rect1.width, rect2.x + rect2.width)
    max_y = max(rect1.y + rect1.height, rect2.y + rect2.height)
    return Rect(min_x, min_y, max_x - min_x, max_y - min_y)
