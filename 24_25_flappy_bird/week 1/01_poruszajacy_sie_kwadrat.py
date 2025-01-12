import pygame

pygame.init()
SZEROKOSC = 400
WYSOKOSC = 600
FPS = 60

zegar = pygame.time.Clock()

ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption('Poruszający się kwadrat')

BIALY = (255, 255, 255)
NIEBIESKI = (0, 0, 255)

# Pozycja kwadratu
pozycja_y = 0  # zaczynamy od góry
predkosc = 2   # kwadrat będzie się poruszał w dół o 2 piksele na klatkę

gra_dziala = True
while gra_dziala:
    for wydarzenie in pygame.event.get():
        if wydarzenie.type == pygame.QUIT:
            gra_dziala = False
    
    # Przesuwamy kwadrat w dół
    pozycja_y = pozycja_y + predkosc
    
    # Gdy kwadrat doleci do dołu, wraca na górę
    if pozycja_y > WYSOKOSC:
        pozycja_y = 0
    
    ekran.fill(BIALY)
    pygame.draw.rect(ekran, NIEBIESKI, (180, pozycja_y, 40, 40))
    
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()