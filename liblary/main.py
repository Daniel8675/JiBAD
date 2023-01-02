# to nie jest zadanie na jeden plik

import csv
import os


def menu(options):
    options = list(options.items())
    for num, option in enumerate(options, start=1):
        print("{}. {}".format(num, option[0]))
    correct_choices = range(1, len(options) + 1)
    while True:
        try:
            choice = int(input(">> "))
            assert choice in correct_choices
            if choice == len(options):
                raise RuntimeError
        except (ValueError, AssertionError):
            pass  # just repeating the while loop
        else:
            func, args, kwargs = options[choice - 1][1]
            return func(*args, **kwargs)


def return_book():
    book_id = int(input("Podaj id ksiazki: "))
    dummy_file = "Books.csv" + ".bak"

    with open("Books.csv", "r") as read_file, open(dummy_file, "w", newline="\n") as write_file:
        csv_reader = csv.reader(read_file)
        csv_writer = csv.writer(write_file, delimiter=",")
        for line in csv_reader:
            try:
                if int(line[0]) == book_id and line[4] == "Wypozyczona":
                    csv_writer.writerow([book_id, line[1], line[2], line[3], "Dostepna"])
                else:
                    csv_writer.writerow(line)
            except ValueError:
                csv_writer.writerow(line)

    os.remove("Books.csv")  # nazwa pliku by mogła być wydzielona do stałej
    os.rename(dummy_file, "Books.csv")

    dummy_file = "Borrowed_Books.csv" + ".bak"

    with open("Borrowed_Books.csv", "r") as read_file, open(dummy_file, "w", newline="\n") as write_file:  # mam deja vu
        csv_reader = csv.reader(read_file)
        csv_writer = csv.writer(write_file, delimiter=",")
        for line in csv_reader:
            try:
                if int(line[0]) == book_id:
                    continue
            except ValueError:
                pass

            csv_writer.writerow(line)

    os.remove("Borrowed_Books.csv")
    os.rename(dummy_file, "Borrowed_Books.csv")


def add_book(): # mieszanie dialogu z użytkownikiem z logiką biznesową
    author = input("Podaj autora: ")
    title = input("Podaj tytul: ")
    keywords = input("Podaj slowa kluczowe: ")
    already_here = False
    book_id = 1

    with open("Books.csv") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for line in csv_reader:
            try:
                book_id = int(line[0]) + 1
                if author == line[1] and title == line[2]:
                    print("Ksiazka juz jest w systemie")
                    already_here = True
            except ValueError:
                pass

    if not already_here:
        with open("Books.csv", "a", newline="\n") as csvfile:
            csv_writer = csv.writer(csvfile, delimiter=",")
            csv_writer.writerow([book_id, author, title, keywords, "Dostepna"])


def remove_book():
    book_id = int(input("Podaj ID ksiazki ktora chcesz usunac: "))
    dummy_file = "Books.csv" + ".bak"

    with open("Books.csv", "r") as read_file, open(dummy_file, "w", newline="\n") as write_file:
        csv_reader = csv.reader(read_file)
        csv_writer = csv.writer(write_file, delimiter=",")
        for line in csv_reader:
            try:
                if int(line[0]) == book_id:
                    continue
            except ValueError:
                pass

            csv_writer.writerow(line)

    os.remove("Books.csv")
    os.rename(dummy_file, "Books.csv")


def add_customer():
    username = input("Podaj nazwe uzytkownika: ")
    password = input("Podaj haslo uzytkownika: ")

    with open("Customers.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            if line[0] == username:
                print("Uzytkownik juz istnieje w systemie.")
                return

    with open("Customers.csv", "a", newline="\n") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerow([username, password])


def search_book_for_customers(username):
    print("Wyszukiwanie ksiązek.\nNastepne pola moga pozostac puste.")
    book_id = input("Podaj id ksiazki: ")
    author = input("Podaj autora: ")
    title = input("Podaj tytul: ")
    keywords = input("Podaj slowa kluczowe: ")

    with open("Books.csv") as csvfile:
        csv_reader = csv.reader(csvfile)
        print(next(csv_reader))
        for line in csv_reader:
            if book_id in line[0] and book_id:
                print(line)
            elif author in line[1] and author:
                print(line)
            elif title in line[2] and title:
                print(line)
            elif keywords in line[3] and keywords:
                print(line)
            elif not (book_id and author and title and keywords):
                print(line)
    try:
        while True:
            menu({
                "Wypozycz ksiazke ": (borrow_book, (username,), {}),
                "Zarezerwuj ksiazke ": (book_book, (username,), {}),
                "Wstecz ": ()
            })
    except RuntimeError:
        pass


def search_book_for_employees():
    print("Wyszukiwanie ksiązek.\nNastepne pola moga pozostac puste.")
    book_id = input("Podaj id ksiazki: ")
    author = input("Podaj autora: ")
    title = input("Podaj tytul: ")
    keywords = input("Podaj slowa kluczowe: ")

    with open("Books.csv") as csvfile:
        csv_reader = csv.reader(csvfile)
        print(next(csv_reader))
        for line in csv_reader:
            if book_id in line[0] and book_id:
                print(line)
            elif author in line[1] and author:
                print(line)
            elif title in line[2] and title:
                print(line)
            elif keywords in line[3] and keywords:
                print(line)
            elif not (book_id and author and title and keywords):
                print(line)

    try:
        while True:
            menu({
                "Zwrot ksiazki ": (return_book, (), {}),
                "Usuniecie ksiazki z katalogu ": (remove_book, (), {}),
                "Wstecz ": (),
            })
    except RuntimeError:
        pass


def borrow_book(username):
    book_id = int(input("Podaj id ksiazki ktora chcesz wypozyczyc: "))
    dummy_file = "Books" + ".bak"
    booked_for_me = False

    with open("Booked_Books.csv") as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            try:
                if int(line[0]) == book_id and line[1] == username:
                    booked_for_me = True
            except ValueError:
                pass

    with open("Books.csv", "r") as read_file, open(dummy_file, "w", newline="\n") as write_file:
        csv_reader = csv.reader(read_file)
        csv_writer = csv.writer(write_file, delimiter=",")
        for line in csv_reader:
            try:
                if int(line[0]) == book_id and line[4] == "Dostepna":
                    csv_writer.writerow([book_id, line[1], line[2], line[3], "Wypozyczona"])
                    print("Ksiazka zostala wypozyczona \n")
                elif int(line[0]) == book_id and booked_for_me is True:
                    csv_writer.writerow([book_id, line[1], line[2], line[3], "Wypozyczona"])
                    print("Ksiazka zostala wypozyczona \n")
                elif int(line[0]) == book_id:
                    print("Ksiazka nie jest dostepna do wypozyczenia. \n")
                    csv_writer.writerow(line)
                else:
                    csv_writer.writerow(line)
            except ValueError:
                csv_writer.writerow(line)

    os.remove("Books.csv")
    os.rename(dummy_file, "Books.csv")

    dummy_file = "Booked_Books" + ".bak"

    with open("Booked_Books.csv", "r") as read_file, open(dummy_file, "w", newline="\n") as write_file:
        csv_reader = csv.reader(read_file)
        csv_writer = csv.writer(write_file, delimiter=",")
        for line in csv_reader:
            try:
                if int(line[0]) == book_id:
                    continue
            except ValueError:
                pass

            csv_writer.writerow(line)

    os.remove("Booked_Books.csv")
    os.rename(dummy_file, "Booked_Books.csv")

    with open("Borrowed_Books.csv", "a", newline="\n") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerow([book_id, username, 14])


def book_book(username):  # świetna nazwa
    book_id = int(input("Podaj id ksiazki ktora chcesz zarezerwowac: "))

    with open("Booked_Books.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            try:
                if int(line[0]) == book_id:
                    print("Ksiazka jest juz zarezerwowana.")
                    return
            except ValueError:
                pass

    dummy_file = "Books.csv" + ".bak"

    with open("Books.csv", "r") as read_file, open(dummy_file, "w", newline="\n") as write_file:
        csv_reader = csv.reader(read_file)
        csv_writer = csv.writer(write_file, delimiter=",")
        for line in csv_reader:
            try:
                if int(line[0]) == book_id:
                    csv_writer.writerow([book_id, line[1], line[2], line[3], "Zarezerwowana"])
                else:
                    csv_writer.writerow(line)
            except ValueError:
                csv_writer.writerow(line)

    os.remove("Books.csv")
    os.rename(dummy_file, "Books.csv")

    with open("Booked_Books.csv", "a", newline="\n") as csvfile:
        csv_writer = csv.writer(csvfile, delimiter=",")
        csv_writer.writerow([book_id, username])


def extend_rental(username):
    with open("Borrowed_Books.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        print("ID KSIAZKI, AUTOR, TYTUL, SLOWA KLUCZOWE, DNI DO ZWROTU")
        for line in csv_reader:
            if line[1] == username:
                with open("Books.csv", "r") as books_file:
                    books_reader = csv.reader(books_file)
                    for row in books_reader:
                        if row[0] == line[0]:
                            print(row, line[2])

    book_id = int(input("Podaj id ksiazki ktorej wypozyczenie chcesz przedluzyc lub podaj 0 by cofnac: "))
    if book_id == 0:
        return
    dummy_file = "Borrowed_Books" + ".bak"

    with open("Borrowed_Books.csv", "r") as read_file, open(dummy_file, "w", newline="\n") as write_file:
        csv_reader = csv.reader(read_file)
        csv_writer = csv.writer(write_file, delimiter=",")
        for line in csv_reader:
            try:
                if int(line[0]) == book_id and line[1] == username:
                    csv_writer.writerow([line[0], line[1], int(line[2]) + 7])
            except ValueError:
                csv_writer.writerow(line)

    os.remove("Borrowed_Books.csv")
    os.rename(dummy_file, "Borrowed_Books.csv")


def customer():
    username = input("Podaj nazwe uzytkownika: ")
    password = input("Podaj haslo: ")
    logged = False

    with open("Customers.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            if username == line[0] and password == line[1]:
                logged = True

    if logged:
        try:
            while True:
                menu({
                    "Przedluz wypozyczenie ": (extend_rental, (username,), {}),
                    "Przegladaj katalog ": (search_book_for_customers, (username,), {}),
                    "Wyloguj ": ()
                })
        except RuntimeError:
            pass
    else:
        print("Podane dane sa bledne.")


def employee():
    employee_id = input("Podaj ID: ")
    password = input("Podaj haslo: ")
    logged = False

    with open("Employees.csv", "r") as csvfile:
        csv_reader = csv.reader(csvfile)
        for line in csv_reader:
            if employee_id == line[0] and password == line[1]:
                logged = True

    if logged:
        try:
            while True:
                menu({
                    "Dodanie ksiazki do katalogu ": (add_book, (), {}),
                    "Dodanie czytelnika ": (add_customer, (), {}),
                    "Przegladaj kataolg ": (search_book_for_employees, (), {}),
                    "Wyloguj": (),
                })
        except RuntimeError:
            pass  # pusty except wymaga komentarza
    else:
        print("Podane dane sa bledne.")


while True:
    try:
        menu({
            "Zaloguj sie jako uzytkownik": (customer, (), {}),
            "Zaloguj sie jako pracownik": (employee, (), {}),
            "Wyjdź": ()
        })
    except RuntimeError:
        exit(1)
