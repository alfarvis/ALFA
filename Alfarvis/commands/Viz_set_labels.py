#!/usr/bin/env python
"""
Set xlabel, ylabel, zlabel
"""

from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)
from .abstract_command import AbstractCommand
from .argument import Argument
from .Viz_Container import VizContainer
from Alfarvis.printers import Printer
from Alfarvis.windows import Window
import matplotlib.pyplot as plt


class VizSetXLabel(AbstractCommand):
    """
    Set label for respective axis
    """

    def briefDescription(self):
        return "set x label"

    def commandType(self):
        return AbstractCommand.CommandType.Visualization

    def __init__(self, axis_label="xlabel"):
        self._axis_label = axis_label

    def commandTags(self):
        """
        Tags to identify the lineplot command
        """
        tags = []
        for word in ["change", "set"]:
            tags.append(word + " " + self._axis_label)
        return tags

    def argumentTypes(self):
        """
        A list of  argument structs that specify the inputs needed for
        executing the lineplot command
        """
        return [Argument(keyword="label", optional=False,
                         tags=[Argument.Tag('as', Argument.TagPosition.After),
                               Argument.Tag('to', Argument.TagPosition.After),
                               Argument.Tag(self._axis_label,
                                            Argument.TagPosition.After)],
                         argument_type=DataType.user_string)]

    def evaluate(self, label):
        """
        Create a line plot 

        """
        result_object = ResultObject(None, None, None, CommandStatus.Error)
        if VizContainer.current_figure is None:
            Printer.Print("No figure available to set x label")
            return result_object
        ax_list = VizContainer.current_figure.axes
        for ax in ax_list:
            if not hasattr(ax_list[0], 'set_' + self._axis_label):
                Printer.Print("Not able to set ", self._axis_label,
                              " for the figure")
                return result_object
            else:
                getattr(ax_list[0], 'set_' +
                        self._axis_label)(' '.join(label.data))
        VizContainer.current_figure.tight_layout()
        VizContainer.current_figure.canvas.draw()
        return ResultObject(None, None, None, CommandStatus.Success)


class VizSetYLabel(VizSetXLabel):
    def briefDescription(self):
        return "set y label"

    def __init__(self):
        super(VizSetYLabel, self).__init__("ylabel")


class VizSetZLabel(VizSetXLabel):
    def briefDescription(self):
        return "set z label"

    def __init__(self):
        super(VizSetZLabel, self).__init__("zlabel")
