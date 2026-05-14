import pygame
# from player import Player
from pomoc import rysuj_poziom, ustaw_ekran
from levels import LEVEL_1

pygame.init()

level = LEVEL_1
screen = ustaw_ekran(level)
pygame.display.set_caption("Backrooms Escape")
clock = pygame.time.Clock()

# player = Player(x=1, y=1)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    rysuj_poziom(screen, level)
    # player.rysuj(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()