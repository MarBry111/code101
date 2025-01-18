import pygame

class Pilka:
    def __init__(self, x, y, kolor):
        # x,y, kolor mozemy pdoać przy tworzeniu
        self.x = x
        self.y = y
        self.kolor = kolor
        # predkosc i rozmiar są stałe dla każdej piłki
        self.predkosc = 2
        self.rozmiar = 30
    
    def ruszaj(self):
        self.x += self.predkosc
        # Gdy pilka wyjdzie poza ekran, wraca na początek
        if self.x > 400:
            self.x = 0
    
    def rysuj(self, ekran):
        pygame.draw.circle(ekran, self.kolor, (self.x, self.y), self.rozmiar)

# Inicjalizacja Pygame
pygame.init()
ekran = pygame.display.set_mode((400, 300))
zegar = pygame.time.Clock()

# Tworzymy kilka piłek w różnych kolorach
pilki = [
    Pilka(0, 50, (255, 0, 0)),    # czerwona
    Pilka(0, 150, (0, 255, 0)),   # zielona
    Pilka(0, 250, (0, 0, 255))    # niebieska
]

# Główna pętla
gra_dziala = True
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False
    
    ekran.fill((255, 255, 255))
    
    # Aktualizujemy i rysujemy wszystkie piłki
    # dla każdej z piłek w lisćie piłki
    for pilka in pilki:
        # ruszaj daną piłką
        pilka.ruszaj()
        # rysuj daną piłkę
        pilka.rysuj(ekran)
    
    pygame.display.flip()
    zegar.tick(60)

pygame.quit()