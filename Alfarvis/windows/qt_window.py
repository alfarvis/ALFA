#!/usr/bin/env python
from .abstract_window import AbstractWindow
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
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
                                      "Figure " + str(self.tab_count))
        self.canvas.mpl_connect('draw_event', self.resizeYLabels)

    def resizeYLabels(self, event):
        bboxes = []
        if len(self.figure.axes) == 0:
            print("No axes to modify")
            return False
        labels = self.figure.axes[0].get_yticklabels()
        for label in labels:
            try:
                bbox = label.get_window_extent()
            except:
                print("Cannot find window extent")
                print(label)
                continue
            # the figure transform goes from relative coords->pixels and we
            # want the inverse of that
            bboxi = bbox.inverse_transformed(self.figure.transFigure)
            bboxes.append(bboxi)

        # this is the bbox that bounds all the bboxes, again in relative
        # figure coords
        bbox = mtransforms.Bbox.union(bboxes)
        # if self.figure.subplotpars.left < bbox.width:
        # we need to move it over
        default_right = 0.9
        scale = 1.1
        if abs(self.figure.subplotpars.left - scale * bbox.width) > 0.01 and (scale * bbox.width < self.figure.subplotpars.right):
            self.figure.subplots_adjust(left=scale * bbox.width)  # pad a little
            self.canvas.draw()
        return False

    @classmethod
    def setParentWidget(self, parent_widget):
        self.parent_tab_widget = parent_widget

    def show(self):
        self.canvas.draw()
        self.parent_tab_widget.setCurrentIndex(self.tab_count)
        # self.canvas.manager.window.activateWindow()
        # self.figure_tab.show()

    def gcf(self):
        return self.figure
