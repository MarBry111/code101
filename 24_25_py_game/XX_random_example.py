# Podpowiedzi jak można wykorzystać random
import random

for i in range(10):
    # Wygenerujemy losową liczbę z zakresu 0-100
    losowa_liczba = random.randint(0, 100)
    print(f'Losowa liczba {i+1}: {losowa_liczba}')

ROZMIAR = 20

for i in range(10):
    # Wygenerujemy losową liczbę z zakresu 0-100 i przeskalujemy do rozmiaru
    losowa_liczba = random.randint(0, 5) * ROZMIAR
    print(f'Losowa liczba {i+1} przeskalowana: {losowa_liczba}')