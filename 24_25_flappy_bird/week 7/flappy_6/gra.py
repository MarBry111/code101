from const import *
from klasy import Rura, Ptak
import pygame

# Włączamy silnik Pygame
pygame.init()

# Zegar gry
zegar = pygame.time.Clock()

# Tworzymy okno gry, gdzie wszystko będziemy wyświetlać
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))

# Dodanie fontu
font = pygame.font.Font(None, 74)

# Ustawiamy tytuł okna
pygame.display.set_caption('Flappy Bird')

# Tworzymy Flappiego i Rurę
flappy = Ptak()
rura = Rura()

punkty = 0

# Główna pętla gry
gra_dziala = True
czekaj = True
while gra_dziala:
    # -------- Sprawdzamy wydarzenia (np. kliknięcia) --------
    for event in pygame.event.get():
        # Jeśli ktoś kliknie X na oknie
        if event.type == pygame.QUIT:
            gra_dziala = False
        # po naciśnieciu SPACJI
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            flappy.skacz()
            # po nacisnięciu spacji przestań czekać
            czekaj = False

    if czekaj:
        # tutaj czekamy więc rysuj tylko flappiego i ekran
        ekran.fill(CZARNY)
        flappy.rysuj(ekran)
    else:
        # cały kod gry
        flappy.spadaj()
        rura.poruszaj()

        # Dodawanie punktów
        if flappy.X == rura.X + rura.SZEROKOSC:
            punkty = punkty + 1

        ekran.fill(CZARNY)
        flappy.rysuj(ekran)
        rura.rysuj(ekran)
        # stwórz obiek z liczbą punktów i wyświetl je na ekranie
        text = font.render(str(punkty), True, (255, 255, 255))
        ekran.blit(text, (0, 0))

    # -------- Pokazujemy wszystko na ekranie --------
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()

