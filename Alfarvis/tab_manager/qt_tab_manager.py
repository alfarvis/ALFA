#!/usr/bin/env python
from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout


def clearLayout(layout):
    while layout.count():
        child = layout.takeAt(0)
        layout.removeItem(child)


class QTabManager(object):
    parent_tab_widget = None
    max_tab_count = 7
    current_index_count = 0

    @classmethod
    def setParentWidget(self, parent_widget):
        self.parent_tab_widget = parent_widget

    @classmethod
    def createTab(self, title):
        if self.parent_tab_widget is None:
            self.parent_tab_widget = QTabWidget()
            self.parent_tab_widget.setMovable(True)

        if self.parent_tab_widget.count() < self.max_tab_count:
            figure_tab = QWidget()
            self.parent_tab_widget.addTab(figure_tab,
                                          title + " " + str(self.current_index_count + 1))
            layout = QVBoxLayout()
        else:
            figure_tab = self.parent_tab_widget.widget(self.current_index_count)
            figure_tab.setWindowTitle(title + " " + str(self.current_index_count + 1))
            layout = figure_tab.layout()
            clearLayout(layout)
        # Update index and connect event
        self.current_index_count = (self.current_index_count + 1) % self.max_tab_count
        return figure_tab, layout
