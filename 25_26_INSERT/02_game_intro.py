# ============= Krok 1 =============
# Najpierw musimy zaimportować potrzebne biblioteki
# pygame - do tworzenia gry
import pygame

# ============= Krok 2 =============
# Musimy włączyć silnik Pygame
# To jak włączenie konsoli do gier!
pygame.init()

# ============= Krok 3 =============
# Ustawiamy rozmiar okna naszej gry
SZEROKOSC = 300
WYSOKOSC = 300
FPS = 60
# Zegar gry
zegar = pygame.time.Clock()

# ============= Krok 4 =============
# Tworzymy okno gry
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
# Ustawiamy tytuł okna
pygame.display.set_caption('Moja Super Gra!')

# ============= Krok 5 =============
# Wybieramy kolory, romziar i połozenie elementu
# Kolory w Pygame to trzy liczby: (R, G, B)
# Każda liczba może być od 0 do 255
BIALY = (255, 255, 255) 
NIEBIESKI = (0, 0, 255)
Y = 150
X = 150
ROZMIAR = 40

# ============= Krok 6 =============
# Główna pętla gry
# To jak filmik, który pokazuje każdą klatkę po kolei
gra_dziala = True
while gra_dziala:
    # -------- Sprawdzamy wydarzenia (np. kliknięcia) --------
    for event in pygame.event.get():
        # Jeśli ktoś kliknie X na oknie
        if event.type == pygame.QUIT:
            # Kończymy grę
            gra_dziala = False
    
    # -------- Rysujemy na ekranie --------
    # Najpierw wypełniamy cały ekran białym kolorem
    ekran.fill(BIALY)
    
    # Rysujemy niebieski kwadrat na środku
    # Parametry to: (gdzie, kolor, (x, y, szerokość, wysokość))
    pygame.draw.rect(ekran, NIEBIESKI, (X, Y, ROZMIAR, ROZMIAR))
    
    # -------- Pokazujemy wszystko na ekranie --------
    # To jak pokazanie gotowego rysunku
    pygame.display.update()
    zegar.tick(FPS)

# ============= Krok 7 =============
# Sprzątamy po sobie (wyłączamy Pygame)
pygame.quit()
quit()

# projekt gry i l;ecimy potem dalej razem
# 1 kółko i krzyżyk?
# 2 asteroids?
# 3 snake?
# 4 flappy bird?
# 5 platformówka?