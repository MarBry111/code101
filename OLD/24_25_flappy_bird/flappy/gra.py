from const import *
from klasy import Rura, Ptak
import pygame

# Włączamy silnik Pygame
pygame.init()

zegar = pygame.time.Clock()

ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
font = pygame.font.Font(None, 74)

pygame.display.set_caption('Flappy Bird')

flappy = Ptak()
rura = Rura()

punkty = 0

# Główna pętla gry
gra_dziala = True
czekaj = True
kolizja = 0
niesmiertelnosc = False

while gra_dziala:
    # -------- Sprawdzamy wydarzenia (np. kliknięcia) --------
    for event in pygame.event.get():
        # Jeśli ktoś kliknie X na oknie
        if event.type == pygame.QUIT:
            gra_dziala = False
        # po naciśnieciu SPACJI
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and kolizja < 3:
            flappy.skacz()
            # po nacisnięciu spacji przestań czekać
            czekaj = False

    if czekaj:
        # jeśli czekaj jest prawdą
        # tutaj czekamy więc rysuj tylko flappiego i ekran
        ekran.fill(CZARNY)
        flappy.rysuj(ekran)
    else:
        ekran.fill(CZARNY)

        flappy.rysuj(ekran)
        rura.rysuj(ekran)
        # stwórz obiek z liczbą punktów i wyświetl je na ekranie
        punkty_txt = font.render(str(punkty), True, BIALY)
        ekran.blit(punkty_txt, (0, 0))

        if kolizja  < 3:
            zycia_txt = font.render('ŻYCIA: '+str(3-kolizja), True, BIALY)
        else:
            zycia_txt = font.render('ŻYCIA: '+str(3-kolizja), True, CZERWONY)
        ekran.blit(zycia_txt, (SZEROKOSC-220, 0))

        if not niesmiertelnosc:
        # kolizja z rurą
            if flappy.X + flappy.ROZMIAR > rura.X and flappy.X < rura.X + rura.SZEROKOSC:
                if flappy.Y < rura.WYSOKOSC1 or flappy.Y + flappy.ROZMIAR > rura.WYSOKOSC1 + rura.PRZERWA:
                    kolizja = kolizja + 1
                    niesmiertelnosc = True

            # kolizja z podłogą
            if flappy.Y + flappy.ROZMIAR >= WYSOKOSC:
                kolizja = kolizja + 1 
                niesmiertelnosc = True

        if kolizja >= 3:
            text = font.render("GAME OVER", True, (255, 0, 0))
            ekran.blit(text, (200, WYSOKOSC//2))
        else:
            # cały kod gry
            # jeśli czekaj nie jest prawdą
            flappy.spadaj()
            rura.poruszaj()

            # Dodawanie punktów
            if flappy.X == rura.X + rura.SZEROKOSC:
                punkty = punkty + 1
                niesmiertelnosc = False

    # -------- Pokazujemy wszystko na ekranie --------
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()

