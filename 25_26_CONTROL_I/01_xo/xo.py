import pygame
from xo_utils import *

pygame.init()

zegar = pygame.time.Clock()
# 01 dodanie fontu
font = pygame.font.Font(None, 55)
ekran = pygame.display.set_mode((SZ, WY))

pygame.display.set_caption('Moja Super Gra!')

plansza = pusta_plansza.copy()

czyj_ruch = 'x'
gra_dziala = True
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False
        # 01 dodanie obslugi klikniecia myszka i zbierania koordynatow
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = pygame.mouse.get_pos()

            k = ktora_kolumna(x)
            w = ktory_wiersz(y)

            # TODO 
            # 02 dodać check czy pole jest puste
            # i tylko wtedy zmienić wartość oraz zmienić gracza

            plansza[w][k] = czyj_ruch
            if czyj_ruch == 'x':   
                czyj_ruch = 'o'
            else:
                czyj_ruch = 'x'
            
            print("Nowa plansza:")
            for p in plansza:
                print(p)

            # TODO
            # 02 sprawdzanie czy ktos wygral

    rysuj_plansze(ekran, plansza)
    # 01 dodanie napisu czyja runda
    text = font.render(f"Ruch: {czyj_ruch}", True, (0, 0, 0))
    ekran.blit(text, (10, 10))
    
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()