import pygame
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
Y = 150
X = 30
ROZMIAR = 30
KROK = ROZMIAR
KIERUNEK = "R"

snake = pygame.Surface((ROZMIAR, ROZMIAR))
snake.fill(ZIELONY)

gra_dziala = True
FRAME = 0
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False

    if FRAME in [0, 29]:
        if KIERUNEK == "R":
            X = X + KROK

    ekran.fill(BIALY)
    ekran.blit(snake, (X, Y))
    
    pygame.display.update()
    zegar.tick(FPS)

    FRAME = FRAME + 1
    if FRAME == 60:
        FRAME = 0

pygame.quit()
quit()