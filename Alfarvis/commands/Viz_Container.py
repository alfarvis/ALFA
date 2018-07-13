#!/usr/bin/env python3
import numpy as np
import collections
from Alfarvis.basic_definitions import (DataType, CommandStatus,
                                        ResultObject)


class VizContainer(object):
    """
    Container for storing states of different visualization
    commands. For now stores the latest figure object
    """
    current_figure = None

    @classmethod
    def createResult(self, figure, array_datas, in_keywords):
        fig_keywords = []
        fig_keywords.append('figure')
        fig_keywords.append(str(figure.number))
        fig_keywords = fig_keywords + in_keywords
        if not isinstance(array_datas, collections.Iterable):
            array_datas = [array_datas]
        # TODO Later try adding some room for error like its there in 70% of the arrays
        common_kl = set.intersection(*[set(array_data.keyword_list) for array_data in array_datas])
        fig_keywords = fig_keywords + list(common_kl)

        result_object = ResultObject(figure, fig_keywords, DataType.figure, CommandStatus.Success, add_to_cache=True)
        result_object.createName(fig_keywords)
        self.current_figure = figure
        return result_object
