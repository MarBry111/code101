class Pokemon:
    imie = ""
    typ = ""
    level = 0

def ustaw_pokemona(pokemon, imie, typ, level):
    pokemon.imie = imie
    pokemon.typ = typ
    pokemon.level = level

def atak(pokemon):
    print(f"{pokemon.imie} używa ataku!")

def przedstaw(pokemon):
    print(f"To jest {pokemon.imie}, typ: {pokemon.typ}, poziom: {pokemon.level}")

def leveluj(pokemon):
    pokemon.level = pokemon.level + 1
    print(f"{pokemon.imie} awansował na poziom {pokemon.level}!")

pikachu = Pokemon()
ustaw_pokemona(pikachu, "Pikachu", "Elektryczny", 5)

przedstaw(pikachu)
atak(pikachu)
leveluj(pikachu)
przedstaw(pikachu)

# 3 inne pokemony, leveluj je, przedstaw i użyj ataku
