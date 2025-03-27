from const import *
import pygame
import random 

class Ptak:
    def __init__(self):
        self.ROZMIAR = 40
        self.KOLOR = ZOTLY

        # ustawiamy flappiego na środku ekranu
        # odpowiednio wysokość/2 - połowa flappiego, i szerokosć/2 - połowa flappiego
        self.Y = WYSOKOSC // 2 - self.ROZMIAR  // 2
        self.X = SZEROKOSC // 2 - self.ROZMIAR  // 2

        # początkowa prędkosć i stałe związane z prędkością
        self.predkosc = 1
        self.SILA_SKOKU = 60  # o ile do góry skoczy FLAPPY
        self.PRZYSPIESZENIE = 0.1

    def skacz(self):
        # przesuń flappiego do góry o siłę skoku
        self.Y = self.Y - self.SILA_SKOKU
        # wyseruj prędkosć spadania
        self.predkosc = 0

    def spadaj(self):
        # Sprawdź czy flappy dotyka dolnej krawędzi ekranu
        if self.Y >= WYSOKOSC - self.ROZMIAR:
            self.Y = WYSOKOSC - self.ROZMIAR
            predkosc = 0
        elif self.Y <= 0:
            self.Y = 0
            self.predkosc = 0

        # porusznie flappim
        self.predkosc = self.predkosc + self.PRZYSPIESZENIE
        self.Y = self.Y + self.predkosc

    def rysuj(self, ekran):
        pygame.draw.rect(ekran, self.KOLOR, (self.X, self.Y, self.ROZMIAR, self.ROZMIAR))

class Rura:
    def __init__(self):
        # zmienne rury
        self.Y = 0
        self.X = SZEROKOSC
        self.SZEROKOSC = 50
        self.PREDKOSC = 5
        self.KOLOR = ZIELONY

        self.WYSOKOSC1 = 50
        self.PRZERWA = 200
        self.WYSOKOSC2 = WYSOKOSC - self.WYSOKOSC1 - self.PRZERWA

    def poruszaj(self):
        # poruszanie rury
        self.X = self.X - self.PREDKOSC
        # kiedy rura poza lewym fregmentem ekranu wtedy przenieś na prawo
        if self.X <= 0:
            self.X = SZEROKOSC

            self.WYSOKOSC1 = random.randint(50, 400)
            self.WYSOKOSC2 = WYSOKOSC - self.WYSOKOSC1 - self.PRZERWA

    def rysuj(self, ekran):
        pygame.draw.rect(ekran, self.KOLOR, (self.X, self.Y, self.SZEROKOSC, self.WYSOKOSC1))
        pygame.draw.rect(ekran, self.KOLOR, (self.X, self.Y + self.WYSOKOSC1 + self.PRZERWA, self.SZEROKOSC, self.WYSOKOSC2))
