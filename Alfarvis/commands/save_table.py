#!/usr/bin/env python3
from Alfarvis.tab_manager.qt_tab_manager import QTabManager
from Alfarvis.basic_definitions.find_numbers import findNumbers
from PyQt5.QtWidgets import QTableWidget, QFileDialog
from Alfarvis.printers import Printer
import csv


def save_table(path, user_conv):
    data_out = findNumbers(user_conv.data, 1)
    if len(data_out) == 0:
        number = QTabManager.current_index_count - 1
    else:
        number = data_out[0].data - 1
    if QTabManager.parent_tab_widget is None:
        Printer.Print("Not in Qt GUI mode! Cannot save tables")
        return False
    current_widget = QTabManager.parent_tab_widget.widget(number)
    if current_widget is not None:
        table = current_widget.findChild(QTableWidget)
        save_table_as_csv(table, path)
    else:
        Printer.Print("No tab available to print yet")
        return False
    return True


def save_table_as_csv(table, path):
    if path is None:
        path = QFileDialog.getSaveFileName(None, 'Save File', '', 'CSV(*.csv)')
        try:
            path = path[0]
        except:
            return
    else:
        path = path.data
    Printer.Print("Saving table as csv: ", path)
    with open(path, 'w') as stream:
        writer = csv.writer(stream)
        header_data = []
        for column in range(table.columnCount()):
            item = table.horizontalHeaderItem(column)
            if item is not None:
                header_data.append(str(item.text()))
            else:
                header_data.append('')
        writer.writerow(header_data)
        for row in range(table.rowCount()):
            rowdata = []
            for column in range(table.columnCount()):
                item = table.item(row, column)
                if item is not None:
                    rowdata.append(
                        str(item.text()))
                else:
                    rowdata.append('')
            writer.writerow(rowdata)
    # try:
    # except:
    #    Printer.Print("Cannot save table")
    #    return
