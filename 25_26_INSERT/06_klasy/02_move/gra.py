import pygame
from player import Player
from pomoc import rysuj_poziom, ustaw_ekran
from levels import LEVEL_1

pygame.init()

level = LEVEL_1
screen = ustaw_ekran(level)
pygame.display.set_caption("Backrooms Escape")

player = Player(x=1, y=1)
clock = pygame.time.Clock()

running = True
frame = 0
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Najpier bez if'a i liczenia klatek (żeby zobaczyli jak zasówa się postać), potem dodajemy ograniczenie do 10 klatek na sekundę
    if frame % 10 == 0:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            player.ruch(0, -1, level)
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            player.ruch(0, 1, level)
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            player.ruch(-1, 0, level)
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            player.ruch(1, 0, level)

    rysuj_poziom(screen, level)
    player.rysuj(screen)

    pygame.display.flip()
    clock.tick(60)

    # To dodajemy jak zauważamy że postać porusza się zbyt szybko
    frame += 1
    if frame > 59:
        frame = 0

pygame.quit()