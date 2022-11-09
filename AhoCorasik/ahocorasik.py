import collections


def substring(patterns):  # ← Funkcja odpowiada za "zlokalizowanie" wzorców które są zawarte w innych wzorcach
    tab1, tab2, tab3 = [], [], []

    for pattern_1 in patterns:
        for pattern_2 in patterns:
            if pattern_1 != pattern_2 and pattern_1 in pattern_2:
                tab1.append(pattern_1)  # ← Tutaj zapisywany jest wzorzec który zawiera się w innym
                tab2.append(pattern_2)  # ← Tutaj zapisywany jest wzorzec w którym zawiera się wzór z tab1
                tab3.append(pattern_2.index(pattern_1) + len(pattern_1) - 1)
                # ↑ Tutaj zapisywany jest ostatni indeks wystapienia wzorca z tab1 zawartego w wzorcu z tab2

    return tab1, tab2, tab3


# noinspection PyUnboundLocalVariable
def pre_build(*patterns):  # ← Funkcja odpowiada za zbudowanie tablicy która zawiera słowniki poszczególnych
    # wierzchołków np. indeks 0 w zbudowanej tablicy będzie zawierał słownik z krawędźiami wychodzącymi z danego
    # wierzchołka oraz wierzchołkami do których dojdziemy

    # patterns = sorted(patterns, key=len)

    tab, vertex = [], 1  # ← vertex == odpowiada za wierzcholek który aktualnie tworzymy
    tab1, tab2, tab3 = substring(patterns)  # ← tab1, tab2, tab3 pewnie nie są "najlepszymi" nazwami ale nic lepszego
    # nie udało mi się wymyślić :/

    for pattern in patterns:
        j, new_edge = 0, False  # ← j == wierzchołek na którym się aktualnie znajdujemy | new_edge == czy znajdujemy
        # sie na nowo powstałej gałęzi/krawędzi
        add = -1  # ← add == jest powiązana z tab3. Jeżeli add osiąga wartość z tab3 to wtedy będzie to sygnałem, że
        # powinniśmy dodać stan akcpeptacji ponieważ dotarliśmy do końca wzorca, który zawiera się w naszym "większym"
        # wzorcu
        for i in pattern:
            add += 1
            try:  # ← tablica początkowo będzie pusta, więc będziemy dostawać IndexError, który "złapany" w bloku
                # except uzupełni naszą tablicę
                if i in tab[j] and new_edge is False:  # ← jezeli dana litera jest juz w drzewie i nie tworzymy nowej
                    # galezi/krawedzi to przesuwamy j (aktualny wierzcholek) po krawedzi zawierajaca nasza litere
                    j = tab[j].get(i)
                elif new_edge:  # ← znajdujemy sie na nowej krawedzi, więc tworzymy kolejne wierzcholki
                    tab.append({i: vertex})
                    vertex += 1
                    j += 1
                else:  # ← tworzymy nowa krawedz
                    tab[j].setdefault(i, vertex)
                    new_edge = True
                    vertex += 1
                    j += 1
            # new_edge powstała w celu obsłużenia przypadkow kiedy dana litera wystepowla w kilku wierzcholkach
            # i litera dodawała się w złym wierzchołku. Nie potrafię teraz przytorzyć przypadku dzięki, któremu
            # dodałem zmienną new_edge ponieważ niestety wziąłem się dopiero za koniec za opisanie kodu zamiast
            # robić to na bieżąco. Przperaszam ale liczę, że w miarę jest jasne co chciałem wskórać zmienna new_edge
            except IndexError:
                tab.append({i: vertex})
                vertex += 1
                j += 1

            if pattern in tab2:  # ← "łapiemy" wzorce które zawierają w sobie inne
                if add == tab3[tab2.index(pattern)]:  # ← jesteśmy na końcu podwzorca
                    dummy_vertex = vertex - 1  # ← zapisujemy jego indeks

        tab.insert(vertex - 1, {'end' + pattern: 'end'})  # ← skończyliśmy z naszym wzorcem więc dodajemy dla niego stan
        # akceptujący

        try:  # ← ten blok odpowiada za dodanie wszystkich podwzorcow, które były w naszym wzorcu
            while pattern in tab2:  # ← dopóki nasz wzorzec jest w tablicy "nadwzorcow"(tab2) obługujemy jego podwzorce
                if tab[dummy_vertex]:
                    index = tab2.index(pattern)
                    tab[dummy_vertex].setdefault('end' + str(tab1[index]), 'end')
                    tab1.pop(index)
                    tab2.pop(index)
                    tab3.pop(index)
                    # ↑ usuwamy wzorce z którymi się "rozprawiliśmy"
        except UnboundLocalError:
            continue

    return tab


def bfs_with_parents(trie, root):  # ← klasyczny bfs, który dodatkowo zapisuje rodzica danego wierzchołka
    visited, queue = [[root, None]], collections.deque([root])

    while queue:
        vertex = queue.popleft()
        for neighbors in trie[vertex].values():
            if (neighbors not in visited) and (neighbors != 'end'):
                visited.append([neighbors, vertex])
                queue.append(neighbors)

    return visited  # ← zwracamy [[wierzchołek, rodzic wierzchołka], ...]


def fail_links(trie, visited):
    links = []

    for tab in visited:
        if tab[1] is None or tab[1] == 0:  # ← korzeń jak i jego dzieci mają fail linka wskazującego na korzeń
            links.append([tab[0], 0])
        else:
            vertex, parent = tab[0], tab[1]
            label = [key for key, value in trie[parent].items() if value == vertex].pop()
            # ↑ wartość krawędzi prowadząca z rodzica do wierzchołka
            while True:
                parent_fail_link = [second for first, second in links if first == parent].pop()
                # ↑ idziemy fail linkiem rodzica
                if label in trie[parent_fail_link]:  # ← jeżeli znaleźliśmy wierzchołek który ma krawędź lablel to
                    # znaleźliśmy fail linka i możemy zakończyć działanie pętli
                    links.append([vertex, trie[parent_fail_link].get(label)])
                    break
                elif parent_fail_link == 0 and not label in trie[0]:  # ← dotarliśmy do korzenia w którym znajdziemy
                    # krawędź label bądź mamy "jokera" który ma każdą wartość
                    links.append([vertex, 0])
                    break
                else:  # ← Jeżeli nie znaleźliśmy krawędzi label w wierzchołku i nie jesteśmy w roocie to przechodzimy
                    # po kolejnym fail linku
                    parent = [second for first, second in visited if first == parent_fail_link].pop()

    return links


def build(*patterns):  # ← "złożenie" w jedną całość tablicy z pre_build poprzez dodanie po kolei indeksów wierzchołka
    # oraz zbudowanie fail linków
    tab, trie = pre_build(*patterns), {}

    for i in range(len(tab)):
        trie.setdefault(i, tab[i])

    return trie, fail_links(trie, bfs_with_parents(trie, 0))


def search(automat, text):
    trie, links = automat
    vertex, result = 0, []

    for index, letter in enumerate(text):
        if not letter.isalpha():  # ← pomijamy znaki białe itd.
            continue

        if letter in trie[vertex]:
            vertex = trie[vertex].get(letter)
            if 'end' in trie[vertex].values():  # ← trafiamy na wierzchołek który jest w stanie akceptującym
                for key in trie[vertex]:  # ← przeglądamy klucze ponieważ stanów akceptujących w jednym wierzchołku
                    # może być więcej niż jeden
                    if 'end' in key and key[-1] == letter:
                        result.append([1 + 3 + index - len(key), key[3:]])
                        # ↑ dodanie 3 jak i rozpoczącie "słowa" key od 3 indeksu wynika z budowy stanu akceptującego
                        # ponieważ kluczem w stanie akceptującym jest słowo które jest konkatenacją "end" oraz "wzorca",
                        # który akceptuje
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


# print(search(build("a", "ab"), "abccab"))
# print(search(build("abc", "aab", "cba"), "aabcbaab"))
# print(search(build("a", "ab", "bc", "bca", "c", "caa"), "abccab"))
# print(search(build("he", "she", "hers", "his"), "ahishers"))
# print(search(build("he", "wor"), "hello world"))
# print(search(build("a", "ab", "bc", "abc", "c", "caa"), "abca"))
# print(search(build("b", "abc"), "abca"))
# print(search(build("abcd", "bc"), "abcd"))
# print(search(build("abc", "bc", "c"), "abc"))
