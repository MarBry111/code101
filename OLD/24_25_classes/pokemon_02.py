imie = "Pikachu"
typ = "Elektryczny"
level = 5

# uzyjmy funkcji żeby uporzdkować trochę kod
def atak(imie):
    print(f"{imie} używa ataku!")

def przedstaw(imie, typ, level):
    print(f"To jest {imie}, typ: {typ}, poziom: {level}")

def leveluj(level):
    nowy_level = level + 1
    print(f"{imie} awansował na poziom {nowy_level}!")
    return nowy_level

przedstaw(imie, typ, level)
atak(imie)
level = leveluj(level)
przedstaw(imie, typ, level)

# 3 inne pokemony, leveluj je, przedstaw i użyj ataku
