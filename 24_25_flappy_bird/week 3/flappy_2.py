import pygame

# Włączamy silnik Pygame
pygame.init()

# Ustawiamy rozmiar okna naszej gry i FPSy
SZEROKOSC = 600
WYSOKOSC = 600
FPS = 60

# Zegar gry
zegar = pygame.time.Clock()

# Tworzymy okno gry, gdzie wszystko będziemy wyświetlać
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))

# Ustawiamy tytuł okna
pygame.display.set_caption('Flappy Bird')

# Wybieramy kolory, romziar i połozenie Flappiego
# Kolory w Pygame to trzy liczby: (R, G, B) z zakresu 0-255
BIALY = (255, 255, 255) 
CZARNY = (0, 0 , 0)

NIEBIESKI = (0, 0, 255)
ZOTLY = (255, 255, 0)
ZIELONY = (0, 255, 0)

FLAPPY_ROZMIAR = 40

# ustawiamy flappiego na środku ekranu
# odpowiednio wysokość/2 - połowa flappiego, i szerokosć/2 - połowa flappiego
FLAPPY_Y = WYSOKOSC // 2 - FLAPPY_ROZMIAR // 2
FLAPPY_X = SZEROKOSC // 2 - FLAPPY_ROZMIAR // 2

# początkowa prędkosć i stałe związane z prędkością
predkosc = 1
SILA_SKOKU = 60  # o ile do góry skoczy FLAPPY
PRZYSPIESZENIE = 0.1

# zmienne rury
RURA_Y = 0
RURA_X = SZEROKOSC
RURA_SZEROKOSC = 50
RURA_WYSOKOSC = WYSOKOSC
RURA_PREDKOSC = 5

# Główna pętla gry
gra_dziala = True

while gra_dziala:
    # -------- Sprawdzamy wydarzenia (np. kliknięcia) --------
    for event in pygame.event.get():
        # Jeśli ktoś kliknie X na oknie
        if event.type == pygame.QUIT:
            gra_dziala = False
        # po naciśnieciu SPACJI
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            # przesuń flappiego do góry o siłę skoku
            FLAPPY_Y = FLAPPY_Y - SILA_SKOKU
            # wyseruj prędkosć spadania
            predkosc = 0

    # Sprawdź czy flappy dotyka dolnej krawędzi ekranu
    if FLAPPY_Y >= WYSOKOSC - FLAPPY_ROZMIAR:
        FLAPPY_Y = WYSOKOSC - FLAPPY_ROZMIAR
        predkosc = 0
    elif FLAPPY_Y <= 0:
        FLAPPY_Y = 0
        predkosc = 0

    # porusznie flappim
    predkosc = predkosc + PRZYSPIESZENIE
    FLAPPY_Y = FLAPPY_Y + predkosc

    # poruszanie rury
    RURA_X = RURA_X - RURA_PREDKOSC
    # kiedy rura poza lewym fregmentem ekranu wtedy przenieś na prawo
    if RURA_X <= 0:
        RURA_X = SZEROKOSC

    # -------- Rysujemy na ekranie --------
    ekran.fill(CZARNY)

    # Rysujemy flappiego
    pygame.draw.rect(ekran, ZOTLY, (FLAPPY_X, FLAPPY_Y, FLAPPY_ROZMIAR, FLAPPY_ROZMIAR))
    # Rysujemy rurę
    pygame.draw.rect(ekran, ZIELONY, (RURA_X, RURA_Y, RURA_SZEROKOSC, RURA_WYSOKOSC))

    # -------- Pokazujemy wszystko na ekranie --------
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()

