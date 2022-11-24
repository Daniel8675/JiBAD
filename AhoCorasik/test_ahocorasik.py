from unittest import TestCase
from ahocorasik import AhoCorasik


class Test(TestCase):

    def test_substring(self):
        self.assertEqual(AhoCorasik.substring(["abc", "aab", "cba"]), ([], [], []))
        self.assertEqual(AhoCorasik.substring(["a", "ab", "bc", "abc", "c", "caa"]),
                         (['a', 'a', 'a', 'a', 'ab', 'bc', 'c', 'c', 'c'],
                          ['ab', 'abc', 'caa', 'caa', 'abc', 'abc', 'bc', 'abc', 'caa'],
                          [0, 0, 1, 2, 1, 2, 1, 2, 0]))

    def test_pre_build(self):
        self.assertEqual(AhoCorasik.pre_build(["abc", "aab", "cba"]),
                         [{'a': 1, 'c': 6},
                          {'b': 2, 'a': 4},
                          {'c': 3}, {'endabc': 'end'},
                          {'b': 5}, {'endaab': 'end'},
                          {'b': 7}, {'a': 8},
                          {'endcba': 'end'}])
        self.assertEqual(AhoCorasik.pre_build(["a", "ab", "bc", "abc", "c", "caa"]),
                         [{'a': 1, 'b': 3, 'c': 6},
                          {'enda': 'end', 'b': 2},
                          {'endab': 'end', 'c': 5},
                          {'c': 4}, {'endbc': 'end', 'endc': 'end', 'enda': 'end', 'endab': 'end'},
                          {'endabc': 'end', 'endbc': 'end'},
                          {'endc': 'end', 'a': 7},
                          {'a': 8, 'enda': 'end', 'endc': 'end'},
                          {'endcaa': 'end', 'enda': 'end'}])

    def test_search1(self):
        automat = AhoCorasik()
        automat.add_pattern("a")
        automat.add_pattern("ab")
        automat.build()
        self.assertEqual(automat.search("abccab"),
                         [[0, 'a'], [0, 'ab'], [4, 'a'], [4, 'ab']])

    def test_search2(self):
        automat = AhoCorasik()
        automat.add_pattern("abc")
        automat.add_pattern("aab")
        automat.add_pattern("cba")
        automat.add_pattern("ccc")
        automat.remove_pattern("ccc")
        automat.build()
        self.assertEqual(automat.search("aabcbaab"),
                         [[0, 'aab'], [1, 'abc'], [3, 'cba'], [5, 'aab']])

    def test_search3(self):
        automat = AhoCorasik()
        automat.add_pattern("a")
        automat.add_pattern("ab")
        automat.add_pattern("bc")
        automat.add_pattern("bca")
        automat.add_pattern("c")
        automat.add_pattern("caa")
        automat.build()
        self.assertEqual(automat.search("abccab"),
                         [[0, 'a'], [0, 'ab'], [1, 'bc'], [2, 'c'], [3, 'c'], [4, 'a'], [4, 'ab']])

    def test_search4(self):
        automat = AhoCorasik()
        automat.add_pattern("abcbc")
        automat.add_pattern("bc")
        automat.add_pattern("c")
        automat.build()
        self.assertEqual(automat.search("abcdefbcac"),
                         [[1, 'bc'], [2, 'c'], [6, 'bc'], [7, 'c'], [9, 'c']])

