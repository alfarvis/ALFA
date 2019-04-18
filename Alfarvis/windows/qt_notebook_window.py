#!/usr/bin/env python
from .abstract_window import AbstractWindow
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QTextCursor, QTextBlockFormat


class QtNotebookWindow(AbstractWindow):
    """
    Simple window that is the same as matplotlib figure window
    """
    parent_notebook = None
    scale_notebook = (0.5, 0.5)

    def __init__(self, *args, **kwargs):
        # Create Figure
        if self.parent_notebook is not None:
            size = self.parent_notebook.frameSize()
            min_size = 1
            dpi = 100.0
            kwargs['figsize'] = (max(min_size, self.scale_notebook[0] * (size.width() / dpi)),
                    max(min_size, self.scale_notebook[1] * (size.height() / dpi)))
            kwargs['dpi'] = dpi
        self.show_count = 0
        self.buf = None
        self.figure = plt.figure(*args, **kwargs)
        self.canvas = FigureCanvas(self.figure)
        self.canvas.mpl_connect('resize_event', self.tight_layout)

    def tight_layout(self, event):
        try:
            self.figure.tight_layout()
        except:
            pass

    def show(self):
        if self.parent_notebook is None:
            print("No parent notebook to print the image to")
            return
        self.figure.tight_layout()
        self.canvas.draw()
        size = self.canvas.size()
        self.buf, (width, height) = self.canvas.print_to_buffer()
        image = QImage(self.buf, width, height, QImage.Format_ARGB32)
        self.parent_notebook.insertImage(image, 'figure_' + str(self.figure.number) + '_' + str(self.show_count))
        self.parent_notebook.resetFontSize()
        self.show_count = self.show_count + 1

    def gcf(self):
        return self.figure
