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

gracz = pygame.Surface((ROZMIAR, ROZMIAR))  
gracz.fill(ZIELONY) 

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

    ekran.fill(BIALY)
    ekran.blit(gracz, (X, Y))
    
    pygame.display.update()
    zegar.tick(FPS)


pygame.quit()
quit()

# TODO:
# 2. Dodaj ograniczenie ruchu do granic okna.
#     gdzie gracz nie moze się znaleźć?
# 3. Dodaj grawitację i możliwość skakania za pomocą spacji
#     kiedy gracz ma spadać? co oznacza "podskoczenie"? co się zmieni?
# 4. Dodaj własny obiekt gracza (np. obrazek lub inny kształt).
#     gracz = pygame.image.load(<sciezka do pliku>)
#     gracz = pygame.transform.scale(gracz, (ROZMIAR, ROZMIAR))
# 5. EXTRA - dodaj liczenie frames (która to klatka gry)

