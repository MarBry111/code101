# Najpierw musimy zaimportować potrzebne biblioteki
import pygame

# To jak włączenie konsoli do gier!
pygame.init()

# Ustawiamy rozmiar okna naszej gry
SZEROKOSC = 600
WYSOKOSC = 600
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
Y = 200
X = 200
JABLKO_X = 100
JABLKO_Y = 100
ROZMIAR = 50

# załadujemy obrazek
jablko_image = pygame.image.load("24_25_py_game/my_sprite.png").convert_alpha()
# Przeskalujemy obrazek do odpowiedniego rozmiaru
jablko_image = pygame.transform.scale(jablko_image, (ROZMIAR, ROZMIAR))

# ============= Krok 6 =============
# Główna pętla gry
gra_dziala = True
while gra_dziala:
    # -------- Sprawdzamy wydarzenia (np. kliknięcia) --------
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gra_dziala = False

        if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
            Y = Y - ROZMIAR
        if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
            Y = Y + ROZMIAR
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
            X = X + ROZMIAR
        if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
            X = X - ROZMIAR

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
    
    # Parametry to: (gdzie, kolor, (x, y, szerokość, wysokość))
    pygame.draw.rect(ekran, ZIEOLONY, (X, Y, ROZMIAR, ROZMIAR))
    # pygame.draw.rect(ekran, ZOLTY, (JABLKO_X, JABLKO_Y, ROZMIAR, ROZMIAR))
    ekran.blit(jablko_image, (JABLKO_X, JABLKO_Y))
    
    # -------- Pokazujemy wszystko na ekranie --------
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()
