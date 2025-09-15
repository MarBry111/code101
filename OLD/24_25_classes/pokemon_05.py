class Pokemon:
    def __init__(self, imie, typ, level):
        self.imie = imie
        self.typ = typ
        self.level = level
    
    def atak(self):
        print(f"{self.imie} używa ataku!")
    
    def przedstaw(self):
        print(f"To jest {self.imie}, typ: {self.typ}, poziom: {self.level}")
    
    def leveluj(self):
        self.level = self.level + 1
        print(f"{self.imie} awansował na poziom {self.level}!")

pikachu = Pokemon("Pikachu", "Elektryczny", 5)

pikachu.przedstaw()
pikachu.atak()
pikachu.leveluj()

# 3 inne pokemony, leveluj je, przedstaw i użyj ataku
# 1 dodaj ograniczenia że może być max 100 level
# 2 dodaj nazwę ataku dla każdego pokemona przy tworzzeniu oraz żeby była użyta przy ataku