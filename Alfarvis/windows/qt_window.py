#!/usr/bin/env python
from .abstract_window import AbstractWindow
import matplotlib.pyplot as plt
#from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from Alfarvis.tab_manager.qt_tab_manager import QTabManager
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar


class QtWindow(AbstractWindow):
    """
    Simple window that is the same as matplotlib figure window
    """

    def __init__(self, *args, **kwargs):
        self.tab_index = QTabManager.current_index_count
        figure_tab, layout = QTabManager.createTab("Figure")
        # Create Figure
        self.figure = plt.figure(*args, **kwargs)
        self.canvas = FigureCanvas(self.figure)
        self.toolbar = NavigationToolbar(self.canvas, figure_tab)
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        figure_tab.setLayout(layout)
        self.canvas.mpl_connect('resize_event', self.tight_layout)

    def tight_layout(self, event):
        try:
            self.figure.tight_layout()
        except:
            pass

    def show(self):
        self.figure.tight_layout()
        self.canvas.draw()
        QTabManager.parent_tab_widget.setCurrentIndex(self.tab_index)

    def gcf(self):
        return self.figure
