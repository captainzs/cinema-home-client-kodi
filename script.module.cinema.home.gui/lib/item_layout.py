from control_item_group import ControlItemGroup


class ItemLayout:
    def __init__(self, width=None, height=None, clazz=None):
        self.__width = width
        self.__height = height
        self.__clazz = clazz
        return

    def width(self):
        return self.__width

    def height(self):
        return self.__height

    def new(self):
        if self.__clazz is None or not issubclass(self.__clazz, ControlItemGroup):
            raise RuntimeError("Can not create controls for item with layout: {}".format(self.__clazz))
        return self.__clazz(self.__width, self.__height)
