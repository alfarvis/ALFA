#!/usr/bin/env python
import unittest
from Alfarvis.history import KeywordSearch


class TestKeywordSearch(unittest.TestCase):

    def testEmptyKeywordSearch(self):
        keyword_search = KeywordSearch()
        out = keyword_search.search(['hello'])
        self.assertEqual(len(out), 0)

    def testAddingKeywords(self):
        keyword_search = KeywordSearch()
        keyword_search.add(['dravid', 'age'], 0)
        keyword_search.add(['dravid', 'batting_average'], 1)
        keyword_search.add(['sachin', 'batting_average'], 2)
        out = keyword_search.search(['dravid'])
        self.assertEqual(out, [0, 1])
        out = keyword_search.search(['batting_average', 'dravid'])
        self.assertEqual(out, [1])
        out = keyword_search.search(['What', 'is', 'dravid', 'age'])
        self.assertEqual(out, [0])
        out = keyword_search.search(['sachin', 'dravid'])
        self.assertEqual(out, [0, 1, 2])

    def testKnownWords(self):
        keyword_search = KeywordSearch()
        keyword_search.add(['dravid', 'age'], 0)
        keyword_search.add(['sachin', 'tendulkar'], 1)
        out_set = keyword_search.known({'sachin', 'age', 'hello', 'dravid'})
        self.assertEqual(out_set, {'sachin', 'dravid', 'age'})

    def testTypos(self):
        keyword_search = KeywordSearch()
        keyword_search.add(['dravid', 'david', 'age'], 0)
        keyword_search.add(['sachin', 'tendulkar'], 1)
        self.assertEqual(keyword_search.correctTypo(
            'drvid'), {'dravid', 'david'})
        self.assertEqual(keyword_search.correctTypo('tendukar'), {'tendulkar'})
        self.assertEqual(keyword_search.correctTypo('sachn'), {'sachin'})

    def testMisspelledKeywords(self):
        keyword_search = KeywordSearch()
        keyword_search.add(['dravid', 'age'], 10)
        keyword_search.add(['dravid', 'batting', 'average'], 11)
        out = keyword_search.search('What is dravid agge'.split())
        self.assertEqual(out, [10])
        out = keyword_search.search('What is battting avelage'.split())
        self.assertEqual(out, [11])

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

if __name__ == '__main__':
    unittest.main()
