import pygame

# Włączamy silnik Pygame
pygame.init()

# Ustawiamy rozmiar okna naszej gry i FPSy
SZEROKOSC = 400
WYSOKOSC = 600
FPS = 60

# Zegar gry
zegar = pygame.time.Clock()

# Tworzymy okno gry, gdzie wszystko będziemy wyświetlać
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))

# Ustawiamy tytuł okna
pygame.display.set_caption('Flappy Bird')

# ============= Krok 5 =============
# Wybieramy kolory, romziar i połozenie Flappiego
# Kolory w Pygame to trzy liczby: (R, G, B) z zakresu 0-255
BIALY = (255, 255, 255) 
CZARNY = (0, 0 , 0)

NIEBIESKI = (0, 0, 255)
ZOTLY = (255, 255, 0)

FLAPPY_ROZMIAR = 40

# ustawiamy flappiego na środku ekranu
# odpowiednio wysokość/2 - połowa flappiego, i szerokosć/2 - połowa flappiego
FLAPPY_Y = WYSOKOSC // 2 - FLAPPY_ROZMIAR // 2
FLAPPY_X = SZEROKOSC // 2 - FLAPPY_ROZMIAR // 2

# początkowa prędkosć i stałe związane z prędkością
predkosc = 1
MAX_PREDKOSC = 5
SILA_SKOKU = 60  # o ile do góry skoczy FLAPPY
PRZYSPIESZENIE = 0.1

# ============= Krok 6 =============
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

    # sprawdź czy prędkosć przekroczyła wartosć krytyczną
    if predkosc < MAX_PREDKOSC:
        # jeśli nie to przyspieszaj
        predkosc = predkosc + PRZYSPIESZENIE
    else: 
        # jeśli tak to stała prędkosć
        predkosc = MAX_PREDKOSC

    # Sprawdź czy flappy dotyka dolnej krawędzi ekranu
    if FLAPPY_Y >= WYSOKOSC - FLAPPY_ROZMIAR:
        FLAPPY_Y = WYSOKOSC - FLAPPY_ROZMIAR
    else:
        # aktualizuj ruch flappiego jesli na ekranie
        FLAPPY_Y = FLAPPY_Y + predkosc


    # -------- Rysujemy na ekranie --------
    ekran.fill(CZARNY)

    # Rysujemy niebieski kwadrat na środku
    pygame.draw.rect(ekran, ZOTLY, (FLAPPY_X, FLAPPY_Y, FLAPPY_ROZMIAR, FLAPPY_ROZMIAR))
    
    # -------- Pokazujemy wszystko na ekranie --------
    pygame.display.update()
    zegar.tick(FPS)

# ============= Krok 7 =============
# Sprzątamy po sobie (wyłączamy Pygame)
pygame.quit()
quit()

