import pygame

# Inicjalizacja Pygame
pygame.init()

# Ustawienia okna
szerokosc_okna = 600
wysokosc_okna = 400
okno = pygame.display.set_mode((szerokosc_okna, wysokosc_okna))
pygame.display.set_caption("Prosty tekst w Pygame")

# Kolory
BIALY = (255, 255, 255)
CZARNY = (0, 0, 0)

# Czcionka
try:
    czcionka = pygame.font.Font(None, 74) # Użyj domyślnej czcionki systemowej
except pygame.error as e:
    print(f"Nie można załadować domyślnej czcionki: {e}")
    czcionka = pygame.font.SysFont('arial', 74) # Alternatywna czcionka

# Renderowanie tekstu
tekst_surface = czcionka.render("Witaj w Pygame!", True, CZARNY)

# Pozycja tekstu (wyśrodkowanie)
tekst_rect = tekst_surface.get_rect(center=(szerokosc_okna // 2, wysokosc_okna // 2))

# Główna pętla gry
uruchomiony = True
while uruchomiony:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            uruchomiony = False

    # Wypełnienie tła
    okno.fill(BIALY)

    # Wyświetlenie tekstu
    okno.blit(tekst_surface, tekst_rect)

    # Aktualizacja wyświetlania
    pygame.display.flip()

# Zakończenie Pygame
pygame.quit()