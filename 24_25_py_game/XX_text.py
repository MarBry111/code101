# Definicja zmiennych
liczba_calkowita = 100
tekst = "Punkty: "

# Konwersja liczby całkowitej na string, aby połączyć ją z innym stringiem
liczba_jako_tekst = str(liczba_calkowita)

# Łączenie stringów (konkatenacja)
pelny_tekst = tekst + liczba_jako_tekst
print("Połączony tekst:", pelny_tekst)

# Drukowanie typów zmiennych
print("Typ zmiennej 'liczba_calkowita':", type(liczba_calkowita))
print("Typ zmiennej 'tekst':", type(tekst))
print("Typ zmiennej 'liczba_jako_tekst':", type(liczba_jako_tekst))

# Bezpośrednie drukowanie liczby i tekstu (Python automatycznie konwertuje dla print)
print("Bezpośrednie drukowanie:", tekst, liczba_calkowita)

# Operacje matematyczne na int
nowa_liczba = liczba_calkowita + 50
print("Nowa liczba po dodaniu 50:", nowa_liczba)

# Próba dodania liczby do stringa bez konwersji (spowoduje błąd)
# print(tekst + liczba_calkowita) # Odkomentowanie tej linii spowoduje TypeError

# Poprawna operacja po konwersji
print("Poprawnie dodany tekst i liczba (po konwersji):", tekst + str(nowa_liczba))