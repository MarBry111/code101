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

Y = 150
X = 150
ROZMIAR = 40

gra_dziala = True
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False
    
    ekran.fill(BIALY)
    pygame.draw.rect(ekran, NIEBIESKI, (X, Y, ROZMIAR, ROZMIAR))

    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()
