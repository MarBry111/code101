# Najpierw musimy zaimportować potrzebne biblioteki
import pygame
import random

# To jak włączenie konsoli do gier!
pygame.init()

# Ustawiamy rozmiar okna naszej gry
ROZMIAR = 100
N_KOLUMNY = 8
N_WIERSZE = 8
SZEROKOSC = N_KOLUMNY * ROZMIAR
WYSOKOSC = N_WIERSZE * ROZMIAR
FPS = 60
# Zegar gry
zegar = pygame.time.Clock()

# Tworzymy okno gry
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
# Ustawiamy tytuł okna
pygame.display.set_caption('Moja Super Gra!')

# Kolory w Pygame to trzy liczby: (R, G, B)
# Każda liczba może być od 0 do 255
BIALY = (255, 255, 255) 
NIEBIESKI = (0, 0, 255)
CZERWONY = (255, 0 ,0)
ZOLTY = (255, 239, 0)
ZIEOLONY = (0, 255, 0)
CZARNY = (0, 0, 0)
Y = ROZMIAR
X = ROZMIAR
JABLKO_X = 2* ROZMIAR
JABLKO_Y = 2 * ROZMIAR
VX = ROZMIAR
VY = 0

czcionka = pygame.font.Font(None, 74)
tekst_surface = czcionka.render("Witaj w Pygame!", True, BIALY)
tekst_rect = tekst_surface.get_rect(center=(SZEROKOSC // 2, WYSOKOSC // 2))

# załadujemy obrazek
jablko_image = pygame.image.load("24_25_py_game/my_sprite.png").convert_alpha()
# Przeskalujemy obrazek do odpowiedniego rozmiaru
jablko_image = pygame.transform.scale(jablko_image, (ROZMIAR, ROZMIAR))


# ============= Krok 6 =============
# Główna pętla gry
gra_dziala = True
petla = 0
punkty = 0
while gra_dziala:
    petla = petla + 1
    if petla > 60:
        petla = 1
    # -------- Sprawdzamy wydarzenia (np. kliknięcia) --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            VY = -ROZMIAR
            VX = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            VY = ROZMIAR
            VX = 0
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            VY = 0
            VX = ROZMIAR
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            VY = 0
            VX = -ROZMIAR
    
    if petla in [20, 40, 60]:
        X  = X + VX
        Y  = Y + VY

    if X == JABLKO_X and Y == JABLKO_Y:
        punkty = punkty + 1
        print("Punkty:", punkty)
        JABLKO_X = random.randint(0, N_KOLUMNY - 1) * ROZMIAR
        JABLKO_Y = random.randint(0, N_WIERSZE - 1) * ROZMIAR

    if X < 0:
        X = SZEROKOSC - ROZMIAR
    if X >= SZEROKOSC:
        X = 0
    if Y < 0:
        Y = WYSOKOSC - ROZMIAR
    if Y >= WYSOKOSC:
        Y = 0
    

    # -------- Rysujemy na ekranie --------
    ekran.fill(CZARNY)
    ekran.blit(tekst_surface, tekst_rect)
    
    # Parametry to: (gdzie, kolor, (x, y, szerokość, wysokość))
    pygame.draw.rect(ekran, ZIEOLONY, (X, Y, ROZMIAR, ROZMIAR))
    # pygame.draw.rect(ekran, ZOLTY, (JABLKO_X, JABLKO_Y, ROZMIAR, ROZMIAR))
    ekran.blit(jablko_image, (JABLKO_X, JABLKO_Y))
    
    # -------- Pokazujemy wszystko na ekranie --------
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()