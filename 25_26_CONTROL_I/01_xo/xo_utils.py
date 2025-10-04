import pygame

ROZMIAR_POLA = 100
SZ = 3 * ROZMIAR_POLA
WY = 3  * ROZMIAR_POLA
FPS = 60

# szerokosc linii
SZ_L = 10

BIALY = (255, 255, 255) 
NIEBIESKI = (0, 0, 255)
CZARNY = (0, 0, 0)

pusta_plansza = [
    [' ', ' ', ' '],
    [' ', ' ', ' '],
    [' ', ' ', ' ']
]

# 01 funkcja  do rysowania planszy
def rysuj_plansze(ekran, plansza=None):
    """Rysuje planszę do gry kółko i krzyżyk"""
    ekran.fill(BIALY)
    pygame.draw.rect(ekran, CZARNY, (SZ/3 - SZ_L/2, 0, SZ_L, SZ))
    pygame.draw.rect(ekran, CZARNY, (2*SZ/3 - SZ_L/2, 0, SZ_L, SZ))
    pygame.draw.rect(ekran, CZARNY, (0, WY/3 - SZ_L/2, WY, SZ_L))
    pygame.draw.rect(ekran, CZARNY, (0, 2*WY/3 - SZ_L/2, WY, SZ_L))

    # TODO
    # 02 dodaj rysowanie x i o na podstawie zmiennej plansza


# TODO 02 JA - wyjasnic o co chodzi i czemu taki kod wystarczy
def ktora_kolumna(x):
    """Zwraca numer kolumny (0, 1, 2) na podstawie współrzędnej x"""
    if x < SZ/3:
        return 0
    elif x < 2*SZ/3:
        return 1
    else:
        return 2
    
def ktory_wiersz(y):
    """Zwraca numer wiersza (0, 1, 2) na podstawie współrzędnej y"""
    if y < WY/3:
        return 0
    elif y < 2*WY/3:
        return 1
    else:
        return 2