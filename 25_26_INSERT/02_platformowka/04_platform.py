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
CZERWONY = (255, 0, 0)
ZIELONY = (0, 255, 0)
Y = 150
X = 150
ROZMIAR = 40
KROK = 10
SKOK = 50

gracz_p = pygame.image.load("code101/25_26_INSERT/02_platformowka/mario.png")
gracz_p = pygame.transform.scale(gracz_p, (ROZMIAR, ROZMIAR))

gracz_l = pygame.transform.flip(gracz_p, True, False)

gracz = gracz_p

gra_dziala = True
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False
        # jeśli wciśnięto jakiś klawisz
        if event.type == pygame.KEYDOWN:
            # sprawdź każdą opcję i daj opcję X lub Y (żeby poruszać się WSAD lub strzałkami)
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                X -= KROK
                gracz = gracz_l
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                X += KROK
                gracz = gracz_p
            elif event.key == pygame.K_SPACE and Y == 260:
                Y -= SKOK
    
    Y = Y + 1

    if X < 0:
        X = 0
    if X > 260:
        X = 260
    if Y < 0:
        Y = 0
    if Y > 260:
        Y = 260

    ekran.fill(BIALY)
    ekran.blit(gracz, (X, Y))
    
    pygame.display.update()
    zegar.tick(FPS)


pygame.quit()
quit()
