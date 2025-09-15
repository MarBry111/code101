# Pora na petle w Pythonie!

# Petle sa uzywane do powtarzania czesci kodu wiele razy
# W Pythonie mamy dwie glowne petle: for i while

# Petla for
for i in range(5):  # range(5) tworzy liczby od 0 do 4
    print("To jest iteracja numer:", i)

for i in ["jabłko", "banan", "czereśnia"]:
    print("Owoce:", i)

for j in range(2, 10, 2):  # od 2 do 9, co 2
    print("Liczba parzysta:", j)


# Petla while
x = 0
while x < 5:  # Dopoki x jest mniejsze od 5
    print("x jest teraz:", x)
    x = x + 1  # Zwiekszamy x o 1, zeby petla kiedys sie skonczyla
