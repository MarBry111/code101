import pygame
import random
pygame.init()

SZEROKOSC = 300
WYSOKOSC = 300
FPS = 60
zegar = pygame.time.Clock()

ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption('Moja Super Gra!')

BIALY = (255, 255, 255) 
NIEBIESKI = (0, 0, 255)
ZIELONY = (0, 255, 0)
CZERWONY = (255, 0, 0)
Y = 150
X = 30
XJ = 150
YJ = 150
ROZMIAR = 30
KROK = ROZMIAR
KIERUNEK = "R"
PUNKTY = 0

snake = pygame.Surface((ROZMIAR, ROZMIAR))
snake.fill(ZIELONY)

jablko = pygame.Surface((ROZMIAR, ROZMIAR))
jablko.fill(CZERWONY)
pygame.draw.rect(jablko, BIALY, (0, 0, ROZMIAR, ROZMIAR), 3) 

gra_dziala = True
FRAME = 0
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                KIERUNEK = "R"
            elif event.key == pygame.K_LEFT:
                KIERUNEK = "L"
            elif event.key == pygame.K_DOWN:
                KIERUNEK = "D"
            elif event.key == pygame.K_UP:
                KIERUNEK = "U"

    if FRAME in [0, 29]:
        if KIERUNEK == "R":
            X = X + KROK
        elif KIERUNEK == "L":
            X = X - KROK
        elif KIERUNEK == "D":
            Y = Y + KROK
        elif KIERUNEK == "U":
            Y = Y - KROK

    if X < 0:
        X = 270
    elif X > 270:
        X = 0  
    if Y < 0:
        Y = 270
    elif Y > 270:
        Y = 0

    if X == XJ and Y == YJ:
        PUNKTY = PUNKTY + 1
        print("Punkty:", PUNKTY)
        XJ = random.randint(0, 9) * ROZMIAR
        YJ = random.randint(0, 9) * ROZMIAR

    ekran.fill(BIALY)
    ekran.blit(jablko, (XJ, YJ))
    ekran.blit(snake, (X, Y))
    
    pygame.display.update()
    zegar.tick(FPS)

    FRAME = FRAME + 1
    if FRAME == 60:
        FRAME = 0

pygame.quit()
quit()