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

def rysuj_plansze(ekran, plansza=None):
    """Rysuje planszę do gry kółko i krzyżyk"""
    ekran.fill(BIALY)
    pygame.draw.rect(ekran, CZARNY, (SZ/3 - SZ_L/2, 0, SZ_L, SZ))
    pygame.draw.rect(ekran, CZARNY, (2*SZ/3 - SZ_L/2, 0, SZ_L, SZ))
    pygame.draw.rect(ekran, CZARNY, (0, WY/3 - SZ_L/2, WY, SZ_L))
    pygame.draw.rect(ekran, CZARNY, (0, 2*WY/3 - SZ_L/2, WY, SZ_L))

    # dodaj rysowanie x i o na podstawie planszy


def ktora_kolumna(x):
    if x < SZ/3:
        return 0
    elif x < 2*SZ/3:
        return 1
    else:
        return 2
    
def ktory_wiersz(y):
    if y < WY/3:
        return 0
    elif y < 2*WY/3:
        return 1
    else:
        return 2