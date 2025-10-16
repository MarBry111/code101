import pygame

SZEROKOSC = 300
WYSOKOSC = 300
FPS = 60

BIALY = (255, 255, 255) 
NIEBIESKI = (0, 0, 255)
CZERWONY = (255, 0, 0)
ZIELONY = (0, 255, 0)
Y = 150
X = 150
ROZMIAR = 40
KROK = 10

class Czolg:
    def __init__(self, x, y, sciezka_do_obrazka, player):
        self.x = x
        self.y = y
        self.obrazek = pygame.image.load(sciezka_do_obrazka)
        self.obrazek = pygame.transform.scale(self.obrazek, (ROZMIAR, ROZMIAR))
        self.player = player
        self.zycia = 3

    def rysuj(self, ekran):
        ekran.blit(self.obrazek, (self.x, self.y))

    def ruszaj(self, event):
        if self.player == 1:
            if event.key == pygame.K_a:
                self.x -= KROK
            elif event.key == pygame.K_d:
                self.x += KROK
            elif event.key == pygame.K_w:
                self.y -= KROK
            elif event.key == pygame.K_s:
                self.y += KROK
        elif self.player == 2:
            if event.key == pygame.K_LEFT:
                self.x -= KROK
            elif event.key == pygame.K_RIGHT:
                self.x += KROK
            elif event.key == pygame.K_UP:
                self.y -= KROK
            elif event.key == pygame.K_DOWN:
                self.y += KROK


class Pocisk:
    def __init__(self, x, y, vx, vy, player):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.player = player