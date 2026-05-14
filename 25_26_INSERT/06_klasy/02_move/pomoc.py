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