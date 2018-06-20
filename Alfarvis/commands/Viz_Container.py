#!/usr/bin/env python3
import numpy as np


class VizContainer(object):
    """
    Container for storing states of different visualization
    commands. For now stores the latest figure object
    """
    current_figure = None
