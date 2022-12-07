def how_many_words(filename): # przydałaby się jakaś dekompozycja
    temp = {}   # najlepsza nazwa zmiennej ever

    with open(filename, "r", encoding='utf-8') as file:  # przesłonięcie symbolu wbudowanego
        for line in file:
            if line:    # pusta linia nam nie zrobi krzywdy
                for word in line.split():
                    correct_word = ""

                    for letter in word:
                        if letter.isalpha():
                            correct_word += letter.lower()  # to jest bardzo niewydajne i źle działa

                    if correct_word != '':
                        temp[correct_word] = temp.get(correct_word, 0) + 1

    sorted_temp = {k: v for k, v in sorted(temp.items(), key=lambda kv: kv[1], reverse=True)}  # można też operator.itemgetter(1)

    return {k: v for k, v in sorted_temp.items() if v == sorted_temp[next(iter(sorted_temp))]}  # to nie jest ranking z remisami


print(how_many_words("potop.txt"))  # {'i': 13335}
