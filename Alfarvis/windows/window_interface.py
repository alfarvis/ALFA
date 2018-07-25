#!/usr/bin/env python
from .abstract_window import AbstractWindow
from .regular_window import RegularWindow


class Window(object):
    selected_window_type = RegularWindow

    @classmethod
    def selectWindowType(self, window_type):
        if not issubclass(window_type, AbstractWindow):
            raise RuntimeError("window not subclass of AbstractWindow")
        self.selected_window_type = window_type

    @classmethod
    def window(self, *args, **kwargs):
        return self.selected_window_type(*args, **kwargs)
