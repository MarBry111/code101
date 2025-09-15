import pygame
import sys

pygame.init()
SZEROKOSC = 400
WYSOKOSC = 600
FPS = 60

zegar = pygame.time.Clock()

ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption('Sterowanie spacją')

BIALY = (255, 255, 255)
NIEBIESKI = (0, 0, 255)

pozycja_y = WYSOKOSC // 2  # zaczynamy na środku
predkosc = 0
przyspieszenie = 0.2
sila_skoku = -5  # o ile do góry skoczy kwadrat

gra_dziala = True
while gra_dziala:
    for wydarzenie in pygame.event.get():
        if wydarzenie.type == pygame.QUIT:
            gra_dziala = False
        # Sprawdzamy czy naciśnięto spację
        if wydarzenie.type == pygame.KEYDOWN:
            if wydarzenie.key == pygame.K_SPACE:
                predkosc = sila_skoku  # ustawiamy prędkość do góry
    
    # Aktualizujemy ruch
    predkosc = predkosc + przyspieszenie
    pozycja_y = pozycja_y + predkosc
    
    ekran.fill(BIALY)
    pygame.draw.rect(ekran, NIEBIESKI, (180, pozycja_y, 40, 40))
    
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()