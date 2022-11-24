def how_many_words(filename):
    temp = {}

    with open(filename, "r", encoding='utf-8') as file:
        for line in file:
            if line:
                for word in line.split():
                    correct_word = ""

                    for letter in word:
                        if letter.isalpha():
                            correct_word += letter.lower()

                    if correct_word != '':
                        temp[correct_word] = temp.get(correct_word, 0) + 1

    sorted_temp = {k: v for k, v in sorted(temp.items(), key=lambda kv: kv[1], reverse=True)}

    return {k: v for k, v in sorted_temp.items() if v == sorted_temp[next(iter(sorted_temp))]}


print(how_many_words("potop.txt"))  # {'i': 13335}
