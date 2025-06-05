# Witaj w interaktywnym przewodniku po listach w Pythonie!

# ----------------------------------------------------
# Funkcja do wyświetlania sekcji o tworzeniu list
# ----------------------------------------------------
def pokaz_tworzenie_list():
    print("\n--- 1. Co to jest lista i jak ją stworzyć? 📝 ---")
    print("Lista to jak magiczny plecak, do którego możesz wkładać różne rzeczy w określonej kolejności.")
    print("Mogą to być liczby, słowa (nazywane stringami), a nawet inne listy!")
    print("Listę tworzymy używając nawiasów kwadratowych [] i oddzielając elementy przecinkami.\n")

    # Przykład 1: Lista ulubionych owoców
    ulubione_owoce = ["jabłko", "banan", "truskawka", "pomarańcza"]
    print("Przykład 1: Moja lista ulubionych owoców:", ulubione_owoce)

    # Przykład 2: Lista liczb
    liczby = [1, 5, 10, 15, 20]
    print("Przykład 2: Lista liczb:", liczby)

    # Przykład 3: Lista z różnymi typami danych
    rozne_rzeczy = ["Ala", 7, "kot", True] # True to wartość logiczna (prawda)
    print("Przykład 3: Lista z różnymi rzeczami:", rozne_rzeczy)

    # Przykład 4: Pusta lista
    pusta_lista = []
    print("Przykład 4: Możemy też stworzyć pustą listę:", pusta_lista)

    print("\n✨ Zadania do sekcji 1: ✨")
    print("1. Stwórz listę o nazwie 'moje_kolory' zawierającą Twoje 3 ulubione kolory.")
    print("2. Stwórz listę o nazwie 'liczby_parzyste' zawierającą liczby parzyste od 2 do 10.")
    print("3. Stwórz listę o nazwie 'moje_dane' zawierającą Twoje imię (jako tekst), wiek (jako liczbę) i ulubione zwierzę (jako tekst).")
    print("   Spróbuj potem wydrukować każdą z tych list za pomocą print()!")

# ----------------------------------------------------
# Funkcja do wyświetlania sekcji o dodawaniu do list
# ----------------------------------------------------
def pokaz_dodawanie_do_list():
    print("\n--- 2. Dodawanie elementów do listy ➕ ---")
    print("Twoja lista może rosnąć! Możesz dodawać do niej nowe elementy.\n")

    zwierzeta = ["pies", "kot"]
    print("Nasza początkowa lista zwierząt:", zwierzeta)

    # Metoda .append() - dodaje element na SAMYM KOŃCU listy
    print("\nUżywamy .append('rybka'):")
    zwierzeta.append("rybka")
    print("Zwierzęta po dodaniu 'rybki' na końcu:", zwierzeta)

    zwierzeta.append("chomik")
    print("Zwierzęta po dodaniu 'chomika' na końcu:", zwierzeta)

    # Metoda .insert() - dodaje element na OKREŚLONEJ POZYCJI (indeksie)
    # Pamiętaj, indeksy liczymy od 0!
    print("\nUżywamy .insert(1, 'papuga'):") # Chcemy wstawić 'papugę' na miejsce o indeksie 1 (drugie miejsce)
    zwierzeta.insert(1, "papuga")
    print("Zwierzęta po wstawieniu 'papugi' na indeksie 1:", zwierzeta)

    # Łączenie list za pomocą operatora +
    print("\nMożemy też połączyć dwie listy:")
    nowe_zwierzeta = ["lew", "tygrys"]
    print("Lista pierwsza:", zwierzeta)
    print("Lista druga:", nowe_zwierzeta)
    wszystkie_zwierzeta = zwierzeta + nowe_zwierzeta
    print("Połączone listy:", wszystkie_zwierzeta)
    print("(Uwaga: oryginalne listy 'zwierzeta' i 'nowe_zwierzeta' nie zmieniły się!)")

    print("\n✨ Zadania do sekcji 2: ✨")
    print("1. Stwórz listę 'zakupy' z elementami: \"chleb\", \"masło\".")
    print("2. Dodaj \"ser\" na koniec listy 'zakupy' używając .append().")
    print("3. Dodaj \"sok\" na początku listy 'zakupy' (czyli na indeksie 0) używając .insert().")
    print("4. Stwórz drugą listę 'slodycze' z elementami: \"czekolada\", \"baton\". Połącz listę 'zakupy' i 'slodycze' w nową listę 'pelne_zakupy'.")
    print("   Wydrukuj wszystkie listy po każdej operacji, aby zobaczyć zmiany.")

# ----------------------------------------------------
# Funkcja do wyświetlania sekcji o iteracji po liście
# ----------------------------------------------------
def pokaz_iteracje_po_liscie():
    print("\n--- 3. Przeglądanie listy (iteracja) - różne sposoby 🚶‍♀️🚶‍♂️ ---")
    print("Iterowanie to jak spacerowanie po każdym elemencie listy, jeden po drugim, aby coś z nim zrobić.\n")

    kolory = ["czerwony", "zielony", "niebieski", "żółty", "fioletowy", "pomarańczowy"]
    print("Nasza lista kolorów:", kolory)

    # Sposób 1: Prosta pętla 'for' - element po elemencie
    print("\nSposób 1: Drukowanie każdego koloru po kolei:")
    print("Zaczynamy pętlę 'for kolor in kolory':")
    for kolor in kolory:
        print(f"  Aktualny kolor to: {kolor}")
    print("Koniec pętli.\n")

    # Sposób 2: Iteracja z indeksem używając enumerate()
    print("Sposób 2: Drukowanie koloru razem z jego pozycją (indeksem):")
    print("Zaczynamy pętlę 'for indeks, kolor in enumerate(kolory)':")
    for indeks, kolor in enumerate(kolory):
        print(f"  Na pozycji {indeks} jest kolor: {kolor}")
    print("Koniec pętli.\n")

    # Sposób 3: Iteracja co drugi element (używając 'krojenia' listy)
    print("Sposób 3: Drukowanie co drugiego koloru (zaczynając od pierwszego):")
    print("Używamy specjalnego zapisu: kolory[::2]")
    # kolory[::2] tworzy NOWĄ, tymczasową listę zawierającą co drugi element
    print("Elementy, które zostaną wybrane przez kolory[::2]:", kolory[::2])
    print("Zaczynamy pętlę 'for kolor in kolory[::2]':")
    for kolor in kolory[::2]: # [start:stop:krok] - pominięcie start i stop oznacza całą listę
        print(f"  Co drugi kolor to: {kolor}")
    print("Koniec pętli.\n")

    # Sposób 4: Iteracja co drugi element (używając range() i indeksów)
    print("Sposób 4: Inny sposób na drukowanie co drugiego koloru (używając range()):")
    print("Będziemy generować indeksy: 0, 2, 4...")
    # len(kolory) to długość listy, czyli 6. range(0, 6, 2) da nam 0, 2, 4.
    print(f"Zaczynamy pętlę 'for i in range(0, len(kolory), 2)': (len(kolory) to {len(kolory)})")
    for i in range(0, len(kolory), 2): # range(start, stop, krok)
        print(f"  Indeks to {i}, więc kolor to: {kolory[i]}")
    print("Koniec pętli.\n")

    # Sposób 5: Iteracja co N-ty element (np. co trzeci)
    print("Sposób 5: Drukowanie co trzeciego koloru:")
    print("Używamy zapisu: kolory[::3]")
    print("Elementy, które zostaną wybrane przez kolory[::3]:", kolory[::3])
    print("Zaczynamy pętlę 'for kolor in kolory[::3]':")
    for kolor in kolory[::3]:
        print(f"  Co trzeci kolor to: {kolor}")
    print("Koniec pętli.\n")

    print("✨ Zadania do sekcji 3: ✨")
    print("1. Masz listę imion: imiona = [\"Ania\", \"Bartek\", \"Celina\", \"Damian\", \"Ewa\", \"Filip\"].")
    print("   a) Używając prostej pętli 'for', przywitaj każde imię (np. \"Witaj, Ania!\").")
    print("   b) Używając pętli z enumerate(), wydrukuj każde imię z jego numerem na liście (np. \"1. Ania\", \"2. Bartek\" itd. - pamiętaj, że indeks to 0, więc musisz dodać 1).")
    print("   c) Wydrukuj co drugie imię z tej listy, zaczynając od Bartka.")
    print("2. Masz listę liczb: liczby_testowe = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10].")
    print("   a) Wydrukuj kwadrat każdej liczby z tej listy (liczba * liczba).")
    print("   b) Wydrukuj tylko liczby parzyste z tej listy (podpowiedź: liczba % 2 == 0 oznacza, że liczba jest parzysta).")

# ----------------------------------------------------
# Funkcja do wyświetlania sekcji o dostępie i usuwaniu
# ----------------------------------------------------
def pokaz_dostep_i_usuwanie():
    print("\n--- 4. Dostęp do elementów, ich zmiana i usuwanie 🎯✂️ ---")
    planety = ["Merkury", "Wenus", "Ziemia", "Mars", "Jowisz"]
    print("Nasza lista planet:", planety)

    # Dostęp do elementów przez indeks
    print("\nOdczytywanie elementów:")
    print("Pierwsza planeta (indeks 0):", planety[0])
    print("Trzecia planeta (indeks 2):", planety[2])
    print("Ostatnia planeta (indeks -1):", planety[-1])

    # Zmiana elementu na danym indeksie
    print("\nZmiana elementu:")
    print("Zmieniamy 'Ziemia' na 'Nasza Ziemia'")
    planety[2] = "Nasza Ziemia"
    print("Planety po zmianie:", planety)

    # Usuwanie elementów
    print("\nUsuwanie elementów:")
    # Metoda .remove() - usuwa pierwsze wystąpienie DANEGO ELEMENTU
    print("Usuwamy 'Mars' używając .remove('Mars')")
    planety.remove("Mars")
    print("Planety po usunięciu 'Marsa':", planety)

    # Słowo kluczowe 'del' - usuwa element o DANYM INDEKSIE
    print("\nUsuwamy element o indeksie 0 (Merkury) używając 'del planety[0]'")
    del planety[0]
    print("Planety po usunięciu elementu o indeksie 0:", planety)

    # Metoda .pop() - usuwa element o DANYM INDEKSIE i go ZWRACA (możemy go zapisać)
    # Jeśli nie podamy indeksu, .pop() usunie OSTATNI element.
    print("\nUsuwamy ostatni element ('Jowisz') używając .pop() i zapisujemy go:")
    usunieta_planeta = planety.pop()
    print("Usunięta planeta:", usunieta_planeta)
    print("Planety po użyciu .pop():", planety)

    print("\n✨ Zadania do sekcji 4: ✨")
    print("1. Stwórz listę 'dni_tygodnia' = [\"Pon\", \"Wt\", \"Śr\", \"Czw\", \"Pt\", \"Sob\", \"Nd\"].")
    print("   a) Wyświetl \"Śr\".")
    print("   b) Zmień \"Nd\" na \"Niedziela\".")
    print("   c) Usuń \"Pon\" z listy.")
    print("   d) Usuń ostatni element z listy i wyświetl, który to był dzień.")
    print("   Wydrukuj listę po każdej modyfikacji.")

# ----------------------------------------------------
# Funkcja do wyświetlania sekcji o innych operacjach
# ----------------------------------------------------
def pokaz_inne_operacje():
    print("\n--- 5. Inne przydatne operacje na listach 🛠️ ---")
    narzedzia = ["młotek", "śrubokręt", "klucz", "kombinerki", "młotek"]
    print("Nasza lista narzędzi:", narzedzia)

    # Długość listy - funkcja len()
    print("\nDługość listy (ile elementów):")
    dlugosc = len(narzedzia)
    print(f"W liście jest {dlugosc} narzędzi.")

    # Sprawdzanie, czy element jest na liście - operator 'in'
    print("\nSprawdzanie, czy element jest na liście:")
    if "śrubokręt" in narzedzia:
        print("'śrubokręt' JEST na liście.")
    else:
        print("'śrubokręt' NIE MA na liście.")

    if "piła" in narzedzia:
        print("'piła' JEST na liście.")
    else:
        print("'piła' NIE MA na liście.")

    # Liczenie wystąpień elementu - metoda .count()
    print("\nLiczenie, ile razy dany element występuje:")
    ile_mlotkow = narzedzia.count("młotek")
    print(f"'młotek' występuje {ile_mlotkow} razy.")
    ile_pil = narzedzia.count("piła")
    print(f"'piła' występuje {ile_pil} razy.")

    # Znajdowanie indeksu elementu - metoda .index()
    # Zwraca indeks PIERWSZEGO wystąpienia. Jeśli elementu nie ma, powoduje błąd!
    print("\nZnajdowanie indeksu elementu:")
    try:
        indeks_klucza = narzedzia.index("klucz")
        print(f"'klucz' znajduje się na indeksie: {indeks_klucza}.")
        # Co jeśli elementu nie ma?
        # indeks_pily = narzedzia.index("piła") # To spowoduje błąd, dlatego jest w try-except
    except ValueError:
        print("'piła' nie została znaleziona na liście, więc .index() zgłosiłby błąd.")

    # Sortowanie listy - metoda .sort() (modyfikuje oryginalną listę)
    # lub funkcja sorted() (tworzy NOWĄ, posortowaną listę)
    print("\nSortowanie listy:")
    liczby_do_sortowania = [5, 1, 8, 3, 2]
    print("Liczby przed sortowaniem:", liczby_do_sortowania)
    liczby_do_sortowania.sort() # Sortuje rosnąco
    print("Liczby po .sort():", liczby_do_sortowania)
    liczby_do_sortowania.sort(reverse=True) # Sortuje malejąco
    print("Liczby po .sort(reverse=True):", liczby_do_sortowania)

    litery = ['c', 'a', 'b', 'e', 'd']
    print("\nLitery przed sortowaniem:", litery)
    posortowane_litery = sorted(litery) # sorted() tworzy nową listę
    print("Nowa lista z posortowanymi literami (oryginał bez zmian):", posortowane_litery)
    print("Oryginalna lista liter:", litery)


    print("\n✨ Zadania do sekcji 5: ✨")
    print("1. Stwórz listę kilku owoców, upewnij się, że jeden owoc powtarza się przynajmniej dwa razy.")
    print("   a) Sprawdź, ile owoców jest na liście.")
    print("   b) Sprawdź, czy \"banan\" jest na Twojej liście.")
    print("   c) Policz, ile razy na liście występuje ten powtarzający się owoc.")
    print("   d) Znajdź indeks pierwszego wystąpienia jednego z owoców.")
    print("   e) Posortuj swoją listę owoców alfabetycznie.")

# ----------------------------------------------------
# Główna część programu - menu
# ----------------------------------------------------
if __name__ == "__main__":
    while True:
        print("\n==============================================")
        print("📖 Interaktywny Przewodnik po Listach w Pythonie 📖")
        print("==============================================")
        print("Wybierz temat, który chcesz poznać:")
        print("1. Co to jest lista i jak ją stworzyć?")
        print("2. Dodawanie elementów do listy")
        print("3. Przeglądanie listy (iteracja) - różne sposoby")
        print("4. Dostęp do elementów, ich zmiana i usuwanie")
        print("5. Inne przydatne operacje na listach")
        print("0. Zakończ program")

        wybor = input("Wpisz numer tematu (0-5): ")

        if wybor == '1':
            pokaz_tworzenie_list()
        elif wybor == '2':
            pokaz_dodawanie_do_list()
        elif wybor == '3':
            pokaz_iteracje_po_liscie()
        elif wybor == '4':
            pokaz_dostep_i_usuwanie()
        elif wybor == '5':
            pokaz_inne_operacje()
        elif wybor == '0':
            print("Do zobaczenia następnym razem! Miłego kodowania! 👋")
            break
        else:
            print("❗ Niepoprawny wybór. Proszę wpisać numer od 0 do 5.")

        input("\nNaciśnij Enter, aby wrócić do menu...")