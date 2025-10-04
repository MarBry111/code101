# Gra tekstow papier-kamien-nozyce
# Czym są imprty - słów kilka
import random
import time

# Wstęp i wyjasnienie zasad
print("Witaj w grze papier-kamien-nozyce!")
print("Zasady są proste:")

# mozliwe opcje
opcje = ['p', 'k', 'n']

# dodac punkty orazx check czy wprowadozno prawidlowa opcje
# + upraszczanie kodu jak tutaj

# sama gra...
while True:
    wybor_g = input("Wybierz papier (p), kamień (k) lub nożyce (n): ")
    wybor_c = random.choice(opcje)
    print(f"Komputer wybrał: {wybor_c}")
    if wybor_g == wybor_c:
        print("Remis!")
    elif (wybor_g == 'p' and wybor_c == 'k') or \
         (wybor_g == 'k' and wybor_c == 'n') or \
         (wybor_g == 'n' and wybor_c == 'p'):
        print("Wygrałeś!")
        break
    else:
        print("Przegrałeś! Spróbuj ponownie.")
        break