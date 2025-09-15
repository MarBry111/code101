import pygame

pygame.init()
SZEROKOSC = 400
WYSOKOSC = 600
FPS = 60

zegar = pygame.time.Clock()

ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption('Przyspieszający kwadrat')

BIALY = (255, 255, 255)
NIEBIESKI = (0, 0, 255)

# Pozycja i ruch kwadratu
pozycja_y = 0
predkosc = 0        # zaczynamy bez prędkości
przyspieszenie = 0.1  # kwadrat będzie przyspieszał w dół

gra_dziala = True
while gra_dziala:
    for wydarzenie in pygame.event.get():
        if wydarzenie.type == pygame.QUIT:
            gra_dziala = False
    
    # Zwiększamy prędkość
    predkosc = predkosc + przyspieszenie
    # Przesuwamy kwadrat
    pozycja_y = pozycja_y + predkosc
    
    # Gdy kwadrat doleci do dołu, wraca na górę
    if pozycja_y > WYSOKOSC:
        pozycja_y = 0
        predkosc = 0  # zerujemy prędkość
    
    ekran.fill(BIALY)
    pygame.draw.rect(ekran, NIEBIESKI, (180, pozycja_y, 40, 40))
    
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()