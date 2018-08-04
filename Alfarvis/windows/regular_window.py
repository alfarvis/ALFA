#!/usr/bin/env python
from .abstract_window import AbstractWindow
import matplotlib.pyplot as plt


class RegularWindow(AbstractWindow):
    """
    Simple window that is the same as matplotlib figure window
    """

    def __init__(self, *args, **kwargs):
        self.figure = plt.figure(*args, **kwargs)

    def show(self):
        plt.show(block=False)
        plt.pause(1e-9)
        self.figure.canvas.draw()
        if hasattr(self.figure.canvas.manager, 'window'):
            self.figure.canvas.manager.window.activateWindow()
            self.figure.canvas.manager.window.raise_()

    def gcf(self):
        return self.figure
