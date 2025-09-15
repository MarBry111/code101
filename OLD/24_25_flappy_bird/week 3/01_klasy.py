import pygame

# Prosty program pokazujący jak działają klasy
# Klasa piłka
class Pilka:
    # ten kod bdzie odpalony kiedy stworzymy piłkę
    # np: Pilka(x, y, kolor)
    # self mówi klasie żeby korzystała z danej piłki (z siebie)
    def __init__(self, x, y, kolor):
        # x,y, kolor mozemy pdoać przy tworzeniu
        self.x = x
        self.y = y
        self.kolor = kolor
        # predkosc i rozmiar są stałe dla każdej piłki
        self.predkosc = 2
        self.rozmiar = 30
    
    # funkcja/metoda do poruszania piłką
    # self - wie że ma ryskować daną piłkę, korzystać z jej danych
    def ruszaj(self):
        self.x += self.predkosc
        # Gdy pilka wyjdzie poza ekran, wraca na początek
        if self.x > 400:
            self.x = 0
    
    # funkcja/metoda do rysowania piłki na ekranie
    # self - rysujemy tą piłkę (self) i gdzie (na ekranie) 
    def rysuj(self, ekran):
        pygame.draw.circle(ekran, self.kolor, (self.x, self.y), self.rozmiar)

# Inicjalizacja Pygame
pygame.init()
ekran = pygame.display.set_mode((400, 300))
zegar = pygame.time.Clock()

# Tworzymy kilka piłki
pilka = Pilka(0, 150, (255, 0, 0))

# Główna pętla
gra_dziala = True
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False
    
    ekran.fill((255, 255, 255))
    
    # aktualizuj piłke
    pilka.ruszaj()
    # rysuj ja na ekranie
    pilka.rysuj(ekran)

    pygame.display.flip()
    zegar.tick(60)

pygame.quit()