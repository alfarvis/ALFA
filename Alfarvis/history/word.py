# Python 3 Spelling Corrector
#
# Copyright 2014 Jonas McCallum.
# Updated for Python 3, based on Peter Norvig's
# 2007 version: http://norvig.com/spell-correct.html
#
# Open source, MIT license
# http://www.opensource.org/licenses/mit-license.php
"""
Word based methods and functions

Author: Jonas McCallum
Modified by Gowtham G(ggarime1[at]jhu[dot]edu)
https://github.com/foobarmus/autocorrect

"""
from itertools import chain

ALPHABET = 'abcdefghijklmnopqrstuvwxyz'


def concat(*args):
    """reversed('th'), 'e' => 'hte'"""
    try:
        return ''.join(args)
    except TypeError:
        return ''.join(chain.from_iterable(args))


class Word(object):
    """container for word-based methods"""

    def __init__(self, word):
        """
        Generate slices to assist with typo
        definitions.

        'the' => (('', 'the'), ('t', 'he'),
                  ('th', 'e'), ('the', ''))

        """
        slice_range = range(len(word) + 1)
        self.slices = tuple((word[:i], word[i:])
                            for i in slice_range)
        self.word = word

    def _deletes(self):
        """th"""
        return {concat(a, b[1:])
                for a, b in self.slices[:-1]}

    def _transposes(self):
        """teh"""
        return {concat(a, reversed(b[:2]), b[2:])
                for a, b in self.slices[:-2]}

    def _replaces(self):
        """tge"""
        return {concat(a, c, b[1:])
                for a, b in self.slices[:-1]
                for c in ALPHABET}

    def _inserts(self):
        """thwe"""
        return {concat(a, c, b)
                for a, b in self.slices
                for c in ALPHABET}

    def stringent_typos(self):
        """letter combinations one typo away from word
           Only additions/transposes allowed"""
        return (self._transposes() |
                self._inserts())

    def typos(self):
        """letter combinations one typo away from word"""
        return (self._deletes() | self._transposes() |
                self._replaces() | self._inserts())

    def double_typos(self):
        """letter combinations two typos away from word"""
        return {e2 for e1 in self.typos()
                for e2 in Word(e1).typos()}

    def stringent_double_typos(self):
        """letter combinations two typos away from word"""
        return {e2 for e1 in self.stringent_typos()
                for e2 in Word(e1).stringent_typos()}
