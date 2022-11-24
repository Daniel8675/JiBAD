import collections

'''
Instrukcja:

1. Tworzymy obiekt klasy AhoCorasik: automat = AhoCorasik()
2. Dodajemy (usuwamy) patterny metodami add_pattern (remove_pattern)
3. Budujemy "drzewo" oraz "fail-linki": automat.build()
   Automat można "wyprintować": print(automat)
4. Szukamy wzorcow w tekscie za pomoca metody search podajac tekst do przeszukania: automat.search(text)

'''


class AhoCorasik:
    def __init__(self, keywords=None):
        if keywords is None:
            keywords = []
        self._keywords = keywords
        self._automat = []

    def __repr__(self):
        if self._automat:
            return "Trie: " + str(self._automat[0]) + "\nFailure-links: " + str(self._automat[1])
        else:
            raise ValueError("You haven't built an automaton yet.")

    def add_pattern(self, word):
        if type(word) is str:
            if word in self._keywords:
                pass
            else:
                self._keywords.append(word.lower())
        else:
            raise ValueError("Pattern must be string!!!")

    def remove_pattern(self, word):
        if type(word) is str:
            if word in self._keywords:
                self._keywords.remove(word)
            else:
                raise ValueError("Pattern does not exist!!!")
        else:
            raise ValueError("Pattern must be string!!!")

    def build(self):
        tab, trie = AhoCorasik.pre_build(self._keywords), {}

        for i in range(len(tab)):
            trie.setdefault(i, tab[i])

        self._automat = [trie, AhoCorasik.fail_links(trie, AhoCorasik.bfs_with_parents(trie, 0))]

        #  return trie, AhoCorasik.fail_links(trie, AhoCorasik.bfs_with_parents(trie, 0))

    def search(self, text):
        trie, links = self._automat
        vertex, result = 0, []

        for index, letter in enumerate(text):
            if not letter.isalpha():
                continue

            letter = letter.lower()

            if letter in trie[vertex]:
                vertex = trie[vertex].get(letter)
                if 'end' in trie[vertex].values():
                    for key in trie[vertex]:
                        if 'end' in key and key[-1] == letter:
                            result.append([1 + 3 + index - len(key), key[3:]])
            else:
                while not letter in trie[vertex]:
                    vertex = [second for first, second in links if first == vertex].pop()

                    if vertex == 0:
                        break

                if not trie[vertex].get(letter) is None:
                    vertex = trie[vertex].get(letter)
                    if 'end' in trie[vertex].values():
                        for key in trie[vertex]:
                            if 'end' in key and key[-1] == letter:
                                result.append([4 + index - len(key), key[3:]])
                else:
                    continue

        return result

    @staticmethod
    def substring(patterns):
        substrings, strings, last_indices = [], [], []

        for pattern_1 in patterns:
            for pattern_2 in patterns:
                if pattern_1 != pattern_2 and pattern_1 in pattern_2:
                    for i in range(len(pattern_2) - len(pattern_1) + 1):
                        if pattern_2[i: i + len(pattern_1)] == pattern_1:
                            substrings.append(pattern_1)
                            strings.append(pattern_2)
                            last_indices.append(i + len(pattern_1) - 1)

        return substrings, strings, last_indices

    @staticmethod
    def pre_build(patterns):
        # patterns = sorted(patterns, key=len)
        tab, vertex = [], 1
        substrings, strings, last_indices = AhoCorasik.substring(patterns)

        for pattern in patterns:
            j, new_edge = 0, False
            add = -1
            start_index = 0
            dummy_vertices = []
            for letter in pattern:
                add += 1
                try:
                    if letter in tab[j] and new_edge is False:
                        j = tab[j].get(letter)
                    elif new_edge:
                        tab.append({letter: vertex})
                        vertex += 1
                        j += 1
                    else:
                        tab[j].setdefault(letter, vertex)
                        new_edge = True
                        vertex += 1
                        j += 1
                except IndexError:
                    tab.append({letter: vertex})
                    vertex += 1
                    j += 1

                if pattern in strings:
                    try:
                        if add == last_indices[strings.index(pattern, start_index)]:
                            start_index = strings.index(pattern, start_index) + 1
                            dummy_vertex = vertex - 1
                            dummy_vertices.append(dummy_vertex)
                    except ValueError:  # 'hers' is not in list
                        pass

            tab.insert(vertex - 1, {'end' + pattern: 'end'})

            counter = 0
            while pattern in strings:
                if tab[dummy_vertices[counter % len(dummy_vertices)]]:
                    index = strings.index(pattern)
                    tab[dummy_vertices[counter % len(dummy_vertices)]].setdefault('end' + str(substrings[index]), 'end')
                    substrings.pop(index)
                    strings.pop(index)
                    last_indices.pop(index)

                    counter += 1

        return tab

    @staticmethod
    def bfs_with_parents(trie, root):
        visited, queue = [[root, None]], collections.deque([root])

        while queue:
            vertex = queue.popleft()
            for neighbors in trie[vertex].values():
                if (neighbors not in visited) and (neighbors != 'end'):
                    visited.append([neighbors, vertex])
                    queue.append(neighbors)

        return visited

    @staticmethod
    def fail_links(trie, visited):
        links = []

        for tab in visited:
            if tab[1] is None or tab[1] == 0:
                links.append([tab[0], 0])
            else:
                vertex, parent = tab[0], tab[1]
                label = [key for key, value in trie[parent].items() if value == vertex].pop()
                while True:
                    parent_fail_link = [second for first, second in links if first == parent].pop()
                    if label in trie[parent_fail_link]:
                        links.append([vertex, trie[parent_fail_link].get(label)])
                        break
                    elif parent_fail_link == 0 and not label in trie[0]:
                        links.append([vertex, 0])
                        break
                    else:
                        parent = [second for first, second in visited if first == parent_fail_link].pop()

        return links
