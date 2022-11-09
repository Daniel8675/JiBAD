from unittest import TestCase
import ahocorasik


class Test(TestCase):

    def test_substring(self):
        self.assertEqual(ahocorasik.substring(["abc", "aab", "cba"]), ([], [], []))
        self.assertEqual(ahocorasik.substring(["a", "ab", "bc", "abc", "c", "caa"]),
                         (['a', 'a', 'a', 'ab', 'bc', 'c', 'c', 'c'], ['ab', 'abc', 'caa', 'abc', 'abc', 'bc',
                                                                       'abc', 'caa'], [0, 0, 1, 1, 2, 1, 2, 0]))

    def test_pre_build(self):
        self.assertEqual(ahocorasik.pre_build("abc", "aab", "cba"),
                         [{'a': 1, 'c': 6},
                          {'b': 2, 'a': 4},
                          {'c': 3},
                          {'endabc': 'end'},
                          {'b': 5},
                          {'endaab': 'end'},
                          {'b': 7},
                          {'a': 8},
                          {'endcba': 'end'}])
        self.assertEqual(ahocorasik.pre_build("a", "ab", "bc", "abc", "c", "caa"),
                         [{'a': 1, 'b': 3, 'c': 6},
                          {'enda': 'end', 'b': 2},
                          {'endab': 'end', 'c': 5},
                          {'c': 4},
                          {'endbc': 'end', 'endc': 'end', 'enda': 'end', 'endab': 'end'},
                          {'endabc': 'end'},
                          {'endc': 'end', 'a': 7},
                          {'a': 8, 'enda': 'end', 'endc': 'end'},
                          {'endcaa': 'end'}])

    def test_bfs_with_parents(self):
        self.assertEqual(ahocorasik.bfs_with_parents(ahocorasik.build("abc", "aab", "cba")[0], 0),
                         [[0, None], [1, 0], [6, 0], [2, 1], [4, 1], [7, 6], [3, 2], [5, 4], [8, 7]])

        self.assertEqual(ahocorasik.bfs_with_parents(ahocorasik.build("a", "ab", "bc", "abc", "c", "caa")[0], 0),
                         [[0, None], [1, 0], [3, 0], [6, 0], [2, 1], [4, 3], [7, 6], [5, 2], [8, 7]])

    def test_fail_links(self):
        self.assertEqual(ahocorasik.fail_links(ahocorasik.build("abc", "aab", "cba")[0],
                                               ahocorasik.bfs_with_parents(ahocorasik.build("abc", "aab", "cba")[0],
                                                                           0)),
                         [[0, 0], [1, 0], [6, 0], [2, 0], [4, 1], [7, 0], [3, 6], [5, 2], [8, 1]])

        self.assertEqual(ahocorasik.fail_links(ahocorasik.build("a", "ab", "bc", "abc", "c", "caa")[0],
                                               ahocorasik.bfs_with_parents(
                                                   ahocorasik.build("a", "ab", "bc", "abc", "c", "caa")[0], 0)),
                         [[0, 0], [1, 0], [3, 0], [6, 0], [2, 3], [4, 6], [7, 1], [5, 4], [8, 1]])

    def test_build(self):
        self.assertEqual(ahocorasik.build("abc", "aab", "cba"),
                         ({0: {'a': 1, 'c': 6},
                           1: {'b': 2, 'a': 4},
                           2: {'c': 3},
                           3: {'endabc': 'end'},
                           4: {'b': 5},
                           5: {'endaab': 'end'},
                           6: {'b': 7},
                           7: {'a': 8},
                           8: {'endcba': 'end'}},
                          [[0, 0], [1, 0], [6, 0], [2, 0], [4, 1], [7, 0], [3, 6], [5, 2], [8, 1]]))

        self.assertEqual(ahocorasik.build("a", "ab", "bc", "abc", "c", "caa"),
                         ({0: {'a': 1, 'b': 3, 'c': 6},
                           1: {'enda': 'end', 'b': 2},
                           2: {'endab': 'end', 'c': 5},
                           3: {'c': 4},
                           4: {'endbc': 'end', 'endc': 'end', 'enda': 'end', 'endab': 'end'},
                           5: {'endabc': 'end'},
                           6: {'endc': 'end', 'a': 7},
                           7: {'a': 8, 'enda': 'end', 'endc': 'end'},
                           8: {'endcaa': 'end'}},
                          [[0, 0], [1, 0], [3, 0], [6, 0], [2, 3], [4, 6], [7, 1], [5, 4], [8, 1]]))

    def test_search(self):
        self.assertEqual(ahocorasik.search(ahocorasik.build("a", "ab"), "abccab"),
                         [[0, 'a'], [0, 'ab'], [4, 'a'], [4, 'ab']])

        self.assertEqual(ahocorasik.search(ahocorasik.build("abc", "aab", "cba"), "aabcbaab"),
                         [[0, 'aab'], [1, 'abc'], [3, 'cba'], [5, 'aab']])

        self.assertEqual(ahocorasik.search(ahocorasik.build("a", "ab", "bc", "bca", "c", "caa"), "abccab"),
                         [[0, 'a'], [0, 'ab'], [1, 'bc'], [2, 'c'], [3, 'c'], [4, 'a'], [4, 'ab']])

        self.assertEqual(ahocorasik.search(ahocorasik.build("he", "she", "hers", "his"), "ahishers"),
                         [[1, 'his'], [3, 'she'], [4, 'he'], [4, 'hers']])

        self.assertEqual(ahocorasik.search(ahocorasik.build("he", "wor"), "hello world"), [[0, 'he'], [6, 'wor']])

        self.assertEqual(ahocorasik.search(ahocorasik.build("a", "ab", "bc", "abc", "c", "caa"), "abca"),
                         [[0, 'a'], [0, 'ab'], [0, 'abc'], [3, 'a']])

        self.assertEqual(ahocorasik.search(ahocorasik.build("b", "abc"), "abca"), [[1, 'b'], [0, 'abc']])

        self.assertEqual(ahocorasik.search(ahocorasik.build("abcd", "bc"), "abcd"), [[1, 'bc'], [0, 'abcd']])

        self.assertEqual(ahocorasik.search(ahocorasik.build("abc", "bc", "c"), "abc"),
                         [[0, 'abc'], [1, 'bc'], [2, 'c']])
