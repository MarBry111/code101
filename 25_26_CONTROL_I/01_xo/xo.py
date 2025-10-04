import pygame
from xo_utils import *

pygame.init()

zegar = pygame.time.Clock()
font = pygame.font.Font(None, 55)
ekran = pygame.display.set_mode((SZ, WY))

pygame.display.set_caption('Moja Super Gra!')

plansza = pusta_plansza.copy()

czyj_ruch = 'x'
gra_dziala = True
while gra_dziala:
    # -------- Sprawdzamy wydarzenia (np. kliknięcia) --------
    for event in pygame.event.get():
        # Jeśli ktoś kliknie X na oknie
        if event.type == pygame.QUIT:
            # Kończymy grę
            gra_dziala = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            k = ktora_kolumna(x)
            w = ktory_wiersz(y)

            # dodać check czy pole jest puste
            # i tylko wtedy zmienić wartość oraz zmienić gracza

            plansza[w][k] = czyj_ruch
            if czyj_ruch == 'x':   
                czyj_ruch = 'o'
            else:
                czyj_ruch = 'x'
            
            print("Nowa plansza:")
            for p in plansza:
                print(p)

    rysuj_plansze(ekran, plansza)
    text = font.render(f"Ruch: {czyj_ruch}", True, (0, 0, 0))
    ekran.blit(text, (10, 10))
    
    # -------- Pokazujemy wszystko na ekranie --------
    pygame.display.update()
    zegar.tick(FPS)

# Sprzątamy po sobie (wyłączamy Pygame)
pygame.quit()
quit()