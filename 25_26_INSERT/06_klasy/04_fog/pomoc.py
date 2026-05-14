import pygame

ROZMIAR = 40
KOLOR_SCIANY = (180, 160, 120)
KOLOR_PODLOGI = (40, 40, 35)

def ustaw_ekran(level):
    """Funkcja do ustawiania ekranu na podstawie poziomu"""
    rows = len(level)
    cols = len(level[0])
    screen = pygame.display.set_mode((cols * ROZMIAR, rows * ROZMIAR))
    return screen

def rysuj_poziom(screen, level):
    """Funkcja do rysowania poziomu na ekranie"""
    for row_idx, row in enumerate(level):
        for col_idx, char in enumerate(row):
            rect = pygame.Rect(col_idx * ROZMIAR, row_idx * ROZMIAR, ROZMIAR, ROZMIAR)
            if char == "#":
                pygame.draw.rect(screen, KOLOR_SCIANY, rect)
            else:
                pygame.draw.rect(screen, KOLOR_PODLOGI, rect)

def rysuj_mgla(level, screen, player):
    """Funkcja do rysowania mgły na planszy, zakrywającej wszystko poza 5x5 obszarem wokół gracza"""
    for y in range(len(level)):
        for x in range(len(level[0])):
            if abs(x - player.x) > 2 or abs(y - player.y) > 2:
                rect = pygame.Rect(x * ROZMIAR, y * ROZMIAR, ROZMIAR, ROZMIAR)
                pygame.draw.rect(screen, (0, 0, 0), rect)