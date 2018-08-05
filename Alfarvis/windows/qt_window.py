#!/usr/bin/env python
from .abstract_window import AbstractWindow
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class QtWindow(AbstractWindow):
    """
    Simple window that is the same as matplotlib figure window
    """
    parent_tab_widget = None

    def __init__(self, *args, **kwargs):
        if self.parent_tab_widget is None:
            QtWindow.parent_tab_widget = QTabWidget()
        self.figure_tab = QWidget()
        self.figure = plt.figure(*args, **kwargs)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.figure_tab)
        layout = QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        self.figure_tab.setLayout(layout)
        self.tab_count = self.parent_tab_widget.count()
        self.parent_tab_widget.addTab(self.figure_tab,
                                      "Figure " + str(self.tab_count + 1))
        self.canvas.mpl_connect('resize_event', self.tight_layout)

    def tight_layout(self, event):
        try:
            self.figure.tight_layout()
        except:
            pass

    @classmethod
    def setParentWidget(self, parent_widget):
        self.parent_tab_widget = parent_widget

    def show(self):
        self.figure.tight_layout()
        self.canvas.draw()
        self.parent_tab_widget.setCurrentIndex(self.tab_count)

    def gcf(self):
        return self.figure
