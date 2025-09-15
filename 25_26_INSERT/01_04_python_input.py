# Pobieranie input w Pythonie
# Input to dane, które użytkownik wpisuje z klawiatury
# Funkcja input() zatrzymuje program i czeka, aż użytkownik coś wpisze
# Po wpisaniu i naciśnięciu Enter, to co użytkownik wpisała zostaje zwrócone jako tekst (string)
# Możemy to przypisać do zmiennej, żeby potem z tym pracować

name = input("Jak masz na imię? ")  # Pytamy użytkownika o imię
print("Cześć,", name)  # Wypisujemy powitanie z imieniem

age = input("Ile masz lat? ")  # Pytamy użytkownika o wiek
print("Masz", age, "lat")  # Wypisujemy wiek

# Pamiętaj, że input zawsze zwraca tekst (string)
# Jeśli potrzebujesz liczby, musisz przekonwertować tekst na liczbę
height = input("Ile masz wzrostu w cm? ")  # Pytamy o wzrost
height = int(height)  # Konwertujemy tekst na liczbę całkowitą
print("Masz", height, "cm wzrostu")  # Wypisujemy wzrost