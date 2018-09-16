#!/usr/bin/env python
from .abstract_window import AbstractWindow
import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        layout.removeItem(child)


class QtWindow(AbstractWindow):
    """
    Simple window that is the same as matplotlib figure window
    """
    parent_tab_widget = None
    max_tab_count = 7
    current_index_count = 0

    def __init__(self, *args, **kwargs):
        if self.parent_tab_widget is None:
            QtWindow.parent_tab_widget = QTabWidget()
            QtWindow.parent_tab_widget.setMovable(True)
        # Create tab widget
        self.tab_index = QtWindow.current_index_count
        if self.parent_tab_widget.count() < self.max_tab_count:
            self.figure_tab = QWidget()
            self.parent_tab_widget.addTab(self.figure_tab,
                                          "Figure " + str(self.tab_index + 1))
            self.layout = QVBoxLayout()
        else:
            self.figure_tab = self.parent_tab_widget.widget(QtWindow.current_index_count)
            self.layout = self.figure_tab.layout()
            clearLayout(self.layout)

        # Create Figure
        self.figure = plt.figure(*args, **kwargs)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, self.figure_tab)
        self.layout.addWidget(self.toolbar)
        self.layout.addWidget(self.canvas)
        self.figure_tab.setLayout(self.layout)
        # Update index and connect event
        QtWindow.current_index_count = (QtWindow.current_index_count + 1) % QtWindow.max_tab_count
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
        # self.figure_tab.setLayout(self.layout)
        self.figure.tight_layout()
        self.canvas.draw()
        self.parent_tab_widget.setCurrentIndex(self.tab_index)

    def gcf(self):
        return self.figure
