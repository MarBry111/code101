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

gracz = pygame.image.load("code101/25_26_INSERT/02_platformowka/mario.png")
gracz = pygame.transform.scale(gracz, (ROZMIAR, ROZMIAR))

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
            elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                X += KROK
            elif event.key == pygame.K_UP or event.key == pygame.K_w:
                Y -= KROK
            elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                Y += KROK
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

# TODO:
# 3. Dodaj grawitację i możliwość skakania za pomocą spacji
#     kiedy gracz ma spadać? co oznacza "podskoczenie"? co się zmieni?
# 6. Dodaj flip postaci prawo lewo w zależności od kierunku ruchu
#     (jak śledzic obecny kierunek ruchu?)
# 7. Rozbudować spadanie i skok - double jump? 
#     (jak śledzić informację czy gracz jest w powietrzu? i ew czy wykorzystał double skok?)