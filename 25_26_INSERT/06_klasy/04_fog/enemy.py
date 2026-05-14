import random
import pygame

class Enemy:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.kolor = (128, 0, 0)
        self.kierunek = random.choice([(1,0),(-1,0),(0,1),(0,-1)])
        self.timer_ruchu = 0
        self.opoznienie_ruchu = 30  # klatki między ruchami

    def ruch(self, level):
        self.timer_ruchu += 1
        if self.timer_ruchu >= self.opoznienie_ruchu:
            self.timer_ruchu = 0
            nx = self.x + self.kierunek[0]
            ny = self.y + self.kierunek[1]
            if (0 <= ny < len(level) and 0 <= nx < len(level[0]) and level[ny][nx] != "#"):
                self.x = nx
                self.y = ny
            else:
                self.kierunek = random.choice([(1,0),(-1,0),(0,1),(0,-1)])

    def rysuj(self, screen):
        px = self.x * 40 + 20
        py = self.y * 40 + 20
        pygame.draw.circle(screen, self.kolor, (px, py), 15)

    def zderzenie_z(self, player):
        return self.x == player.x and self.y == player.y