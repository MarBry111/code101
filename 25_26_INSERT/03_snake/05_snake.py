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
Y = [150]
X = [30]
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

glowa = pygame.Surface((ROZMIAR, ROZMIAR))
glowa.fill(NIEBIESKI)

gra_dziala = True
FRAME = 0
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and KIERUNEK != "L":
                KIERUNEK = "R"
            elif event.key == pygame.K_LEFT and KIERUNEK != "R":
                KIERUNEK = "L"
            elif event.key == pygame.K_DOWN and KIERUNEK != "U":
                KIERUNEK = "D"
            elif event.key == pygame.K_UP and KIERUNEK != "D":
                KIERUNEK = "U"

    if FRAME in [0, 29]:
        for i in range(len(X)-1, 0, -1):
            X[i] = X[i-1]
            Y[i] = Y[i-1]

        if KIERUNEK == "R":
            X[0] = X[0] + KROK
        elif KIERUNEK == "L":
            X[0] = X[0] - KROK
        elif KIERUNEK == "D":
            Y[0] = Y[0] + KROK
        elif KIERUNEK == "U":
            Y[0] = Y[0] - KROK

    if X[0] < 0:
        X[0] = 270
    elif X[0] > 270:
        X[0] = 0  
    if Y[0] < 0:
        Y[0] = 270
    elif Y[0] > 270:
        Y[0] = 0

    if X[0] == XJ and Y[0] == YJ:
        PUNKTY = PUNKTY + 1
        print("Punkty:", PUNKTY)
        X.append(X[-1])
        Y.append(Y[-1])
        waz_na_jablku = True
        while waz_na_jablku:
            waz_na_jablku = False
            XJ = random.randint(0, 9) * ROZMIAR
            YJ = random.randint(0, 9) * ROZMIAR
            for x, y in zip(X,Y):
                if x == XJ and y == YJ:
                    waz_na_jablku = True
                    break


    ekran.fill(BIALY)
    ekran.blit(jablko, (XJ, YJ))

    ekran.blit(glowa, (X[0], Y[0]))
    for x, y in zip(X[1:], Y[1:]):
        ekran.blit(snake, (x, y))
    
    pygame.display.update()
    zegar.tick(FPS)

    FRAME = FRAME + 1
    if FRAME == 60:
        FRAME = 0

pygame.quit()
quit()