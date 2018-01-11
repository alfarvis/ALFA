#!/usr/bin/env python

from Alfarvis import create_alpha_module_dictionary
from Alfarvis.alpharvis_versions.abstract_alpha import AbstractAlpha

class AlphaVersionConflict(AbstractAlpha):
    @classmethod
    def _get_version(self):
        return 1.0

def test_creating_alpha_dictionary():
    alpha_module_dictionary = create_alpha_module_dictionary()
    Alpha_1_0 = alpha_module_dictionary[1.0]
