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
Y = 150
X = 150
ROZMIAR = 40

gracz = pygame.Surface((ROZMIAR, ROZMIAR))  
gracz.fill(CZERWONY) 

gra_dziala = True
frame = 0
angle = 0
while gra_dziala:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False

    ekran.fill(BIALY)
    ekran.blit(gracz, (X, Y))
    
    pygame.display.update()
    zegar.tick(FPS)


pygame.quit()
quit()

# TODO:
# 0. Dodaj inne kolory
# 1. Dodaj ruch w lewo i prawo za pomocą strzałek.
#     gdzie pownny się znaleść sprawdzenia nacisnięcia klawiszy?
# 2. Dodaj ograniczenie ruchu do granic okna.
#     gdzie gracz nie moze się znaleźć?
# 3. Dodaj grawitację i możliwość skakania za pomocą spacji
#     kiedy gracz ma spadać? co oznacza "podskoczenie"? co się zmieni?
# 4. Dodaj własny obiekt gracza (np. obrazek lub inny kształt).
#     gracz = pygame.image.load(<sciezka do pliku>)
#     gracz = pygame.transform.scale(gracz, (ROZMIAR, ROZMIAR))
# 5. EXTRA - dodaj liczenie fames (która to klatka gry)

