#!/usr/bin/env python
import unittest
from Alfarvis.history import KeywordSearch

class TestKeywordSearch(unittest.TestCase):
    def testEmptyKeywordSearch(self):
        keyword_search = KeywordSearch()
        out = keyword_search.search(['hello'])
        self.assertEqual(len(out), 0)
        keyword_search.discard(['helwo'], 0)

    def testAddingKeywords(self):
        keyword_search = KeywordSearch()
        keyword_search.add(['dravid', 'age'], 0)
        keyword_search.add(['dravid', 'batting_average'], 1)
        keyword_search.add(['sachin', 'batting_average'], 2)
        out = keyword_search.search(['dravid'])
        self.assertEqual(out, [0, 1])
        out = keyword_search.search(['batting_average','dravid'])
        self.assertEqual(out, [1])
        out = keyword_search.search(['What', 'is', 'dravid', 'age'])
        self.assertEqual(out, [0])
        out = keyword_search.search(['sachin','dravid'])
        self.assertEqual(out, [])

    def testRemovingKeywords(self):
        keyword_search = KeywordSearch()
        keyword_search.add(['hello'], 0)
        keyword_search.add(['world'], 1)
        out = keyword_search.search(['hello'])
        self.assertEqual(out, [0])
        keyword_search.discard(['hello', 'world'], 0)
        out = keyword_search.search(['hello'])
        self.assertEqual(out, [])
        out = keyword_search.search(['world'])
        self.assertEqual(out, [1])
