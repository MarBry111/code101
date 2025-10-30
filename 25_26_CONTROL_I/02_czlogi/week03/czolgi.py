import pygame
from czolgi_utils import *
pygame.init()

zegar = pygame.time.Clock()

ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption('CZOLGI')

gracz = pygame.Surface((ROZMIAR, ROZMIAR))  
gracz.fill(ZIELONY)

cz1 = Czolg(0, 130, 'code101\\25_26_CONTROL_I\\02_czlogi\\tank1.png', 1)
cz2 = Czolg(260, 130, 'code101\\25_26_CONTROL_I\\02_czlogi\\tank2.png', 2)

pociski = []

gra_dziala = True
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False
        if event.type == pygame.KEYDOWN:
            cz1.obrot(event)
            cz2.obrot(event)

            if event.key == pygame.K_SPACE:
                p = cz1.strzel()
                pociski.append(p)
            if event.key == pygame.K_RETURN:
                p = cz2.strzel()
                pociski.append(p)

            cz1.ruszaj(event)
            cz2.ruszaj(event)

    ekran.fill(BIALY)
    cz1.rysuj(ekran)
    cz2.rysuj(ekran)

    for p in pociski:
        p.ruszaj()
        p.rysuj(ekran)

        if p.hitbox.colliderect(cz1.hitbox) and p.player == 2:
            print("Czolg 1 trafiony!")
        if p.hitbox.colliderect(cz2.hitbox) and p.player == 1:
            print("Czolg 2 trafiony!")
    
    pygame.display.update()
    zegar.tick(FPS)


pygame.quit()
quit()
