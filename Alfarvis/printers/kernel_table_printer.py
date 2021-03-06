#!/usr/bin/env python
from .abstract_table_printer import AbstractTablePrinter
from .align import Align


class KernelTablePrinter(AbstractTablePrinter):
    """
    Table printer for the kernel
    """

    def mapAlignment(self, alignment):
        if alignment == Align.Left:
            return '<'
        elif alignment == Align.Right:
            return '>'
        elif alignment == Align.Center:
            return '^'
        raise RuntimeError("Do not understoond align")

    def initialize(self, ncols, col_widths=None, headers=None,
                   alignments=None, **kwargs):
        """
        Initialize the table
        """
        if alignments is None:
            alignments = [Align.Left] * ncols
        if col_widths is None:
            col_widths = [20] * ncols
        row_format = ''
        for alignment, col_width in zip(alignments, col_widths):
            align_char = self.mapAlignment(alignment)
            col_width_str = str(int(col_width))
            row_format = row_format + '{:' + align_char + col_width_str + '} '
        self.row_format = row_format
        print(row_format.format(*headers))

    def addRow(self, row_names, color_fill=None):
        """
        Add data to table
        """
        print(self.row_format.format(*row_names))

    def show(self):
        """
        No need since we print it as soon as we add a row
        """
        return
