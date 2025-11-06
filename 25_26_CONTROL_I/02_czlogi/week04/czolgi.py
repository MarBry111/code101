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

serce = pygame.surface.Surface((20, 20))
serce.fill(BIALY)
pygame.draw.circle(serce, CZERWONY, (10,10), 9)

pociski = []

font = pygame.font.SysFont(None, 55)
tekst = font.render('GAME OVER!', True, CZERWONY)

gra_dziala = True
gra_refresh = True
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False
        if event.type == pygame.KEYDOWN and gra_refresh:
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
    for i in range(cz1.zycia):
        ekran.blit(serce, (i*20, 0))
    for i in range(cz2.zycia):
        ekran.blit(serce, (SZEROKOSC - (i+1)*20, 0))

    for p in pociski:
        p.ruszaj()
        p.rysuj(ekran)

        if p.hitbox.colliderect(cz1.hitbox) and p.player == 2:
            pociski.remove(p)
            cz1.zycia = cz1.zycia - 1
        if p.hitbox.colliderect(cz2.hitbox) and p.player == 1:
            pociski.remove(p)
            cz2.zycia = cz2.zycia - 1
    
    if cz1.zycia <= 0 or cz2.zycia <= 0:
        gra_refresh = False
        ekran.blit(tekst, (SZEROKOSC//2 - tekst.get_width()//2, WYSOKOSC//2 - tekst.get_height()//2))

    pygame.display.update()
    zegar.tick(FPS)


pygame.quit()
quit()
