# To jest nasz pierwszy program w Pygame!
# Będziemy tworzyć grę Flappy Bird, ale zaczniemy od podstaw
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
# Wybieramy kolory, romziar i połozenie Flappiego
# Kolory w Pygame to trzy liczby: (R, G, B)
# Każda liczba może być od 0 do 255
BIALY = (255, 255, 255) 
NIEBIESKI = (0, 0, 255)
FLAPPY_Y = 150
FLAPPY_X = 150
FLAPPY_ROZMIAR = 40
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
    pygame.draw.rect(ekran, NIEBIESKI, (FLAPPY_X, FLAPPY_Y, FLAPPY_ROZMIAR, FLAPPY_ROZMIAR))
    
    # -------- Pokazujemy wszystko na ekranie --------
    # To jak pokazanie gotowego rysunku
    pygame.display.update()
    zegar.tick(FPS)
# ============= Krok 7 =============
# Sprzątamy po sobie (wyłączamy Pygame)
pygame.quit()
quit()
# ============= ZADANIA DO ZROBIENIA =============
# 1. Zmień rozmiar okna
# 2. Dodaj inne kolory - spóbuj dostać żółty
# 3. Przesuń Flappiego w inne miejsce
# 4. Ustaw Flappiego na środku ekranu (czy obie zmienne będa się zmieniać - X i Y?)
# 5. Spraw żeby kwadrat poruszał się w dół
# 6. Spraw żeby kwadrat przyspieszał w dół (poruszał się coraz szybciej i jak dotrze na dół  - przenieś go na górę)
# 7. Spraw żeby spacja powodowała "skok" flappiego
# 8. Kiedy Flappy dotrze na górę albo na dół zatrzymaj go (ma przestać sie poruszać i nie wystawać poza ekran)