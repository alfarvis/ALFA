#!/usr/bin/env python3
import unittest
from Alfarvis.basic_definitions.find_numbers import (getNumber, findNumbers)


class TestFindNumbers(unittest.TestCase):
    def test_get_number(self):
        self.assertEqual(getNumber('2.0'), 2.0)
        self.assertEqual(getNumber('2'), 2)
        self.assertEqual(getNumber('-1.0'), -1)
        self.assertEqual(getNumber('100,000'), None)
        self.assertEqual(getNumber('100R'), None)

    def test_find_numbers(self):
        res = findNumbers(['2', 'and', '4'], 2)
        self.assertEqual(res[0].data, 2)
        self.assertEqual(res[1].data, 4)
        res = findNumbers(['2', 'and', '4'], 1)
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0].data, 2)
