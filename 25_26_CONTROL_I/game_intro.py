import pygame
pygame.init()

SZEROKOSC = 300
WYSOKOSC = 300
FPS = 60

zegar = pygame.time.Clock()


ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))
pygame.display.set_caption('Moja Super Gra!')

BIALY = (255, 255, 255) 
NIEBIESKI = (0, 0, 255)
Y = 150
X = 150
ROZMIAR = 40

gra_dziala = True
while gra_dziala:
    # -------- Sprawdzamy wydarzenia (np. kliknięcia) --------
    for event in pygame.event.get():
        # Jeśli ktoś kliknie X na oknie
        if event.type == pygame.QUIT:
            # Kończymy grę
            gra_dziala = False
    

    ekran.fill(BIALY)
    pygame.draw.rect(ekran, NIEBIESKI, (X, Y, ROZMIAR, ROZMIAR))
    
    # -------- Pokazujemy wszystko na ekranie --------
    pygame.display.update()
    zegar.tick(FPS)

# Sprzątamy po sobie (wyłączamy Pygame)
pygame.quit()
quit()