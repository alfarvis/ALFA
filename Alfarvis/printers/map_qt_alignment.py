#!/usr/bin/env python
from .align import Align
from PyQt5.QtCore import Qt


def mapAlignment(alignment):
    if alignment == Align.Left:
        return Qt.AlignLeft
    elif alignment == Align.Right:
        return Qt.AlignRight
    elif alignment == Align.Center:
        return Qt.AlignCenter
    raise RuntimeError("Do not understand alignment")
