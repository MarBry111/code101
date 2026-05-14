import pygame
from pomoc import ROZMIAR

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 3
        self.kolor = (255, 220, 100)
        self.rozmiar = ROZMIAR

    def rysuj(self, screen):
        px = self.x * self.rozmiar + self.rozmiar // 2
        py = self.y * self.rozmiar + self.rozmiar // 2
        pygame.draw.circle(screen, self.kolor, (px, py), self.rozmiar // 3)

    def moze_sie_ruszyc(self, dx, dy, level):
        new_x = self.x + dx
        new_y = self.y + dy
        if 0 <= new_y < len(level) and 0 <= new_x < len(level[0]) and level[new_y][new_x] != "#":
            return True
        else:
            return False

    def ruch(self, dx, dy, level):
        if self.moze_sie_ruszyc(dx, dy, level):
            self.x += dx
            self.y += dy