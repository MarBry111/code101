import pygame

# Włączamy silnik Pygame
pygame.init()

# Ustawiamy rozmiar okna naszej gry i FPSy
SZEROKOSC = 600
WYSOKOSC = 600
FPS = 60

# Zegar gry
zegar = pygame.time.Clock()

# Tworzymy okno gry, gdzie wszystko będziemy wyświetlać
ekran = pygame.display.set_mode((SZEROKOSC, WYSOKOSC))

# Ustawiamy tytuł okna
pygame.display.set_caption('Flappy Bird')

# Wybieramy kolory, romziar i połozenie Flappiego
# Kolory w Pygame to trzy liczby: (R, G, B) z zakresu 0-255
BIALY = (255, 255, 255) 
CZARNY = (0, 0 , 0)

NIEBIESKI = (0, 0, 255)
ZOTLY = (255, 255, 0)
ZIELONY = (0, 255, 0)

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
        self.WYSOKOSC = WYSOKOSC
        self.PREDKOSC = 5
        self.KOLOR = ZIELONY

    def poruszaj(self):
        # poruszanie rury
        self.X = self.X - self.PREDKOSC
        # kiedy rura poza lewym fregmentem ekranu wtedy przenieś na prawo
        if self.X <= 0:
            self.X = SZEROKOSC

    def rysuj(self, ekran):
        pygame.draw.rect(ekran, self.KOLOR, (self.X, self.Y, self.SZEROKOSC, self.WYSOKOSC))


flappy = Ptak()
rura = Rura()

# Główna pętla gry
gra_dziala = True

while gra_dziala:
    # -------- Sprawdzamy wydarzenia (np. kliknięcia) --------
    for event in pygame.event.get():
        # Jeśli ktoś kliknie X na oknie
        if event.type == pygame.QUIT:
            gra_dziala = False
        # po naciśnieciu SPACJI
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            flappy.skacz()

    flappy.spadaj()
    rura.poruszaj()

    # -------- Rysujemy na ekranie --------
    ekran.fill(CZARNY)
    # Rysujemy flappiego
    flappy.rysuj(ekran)
    # Rysujemy rurę
    rura.rysuj(ekran)

    # -------- Pokazujemy wszystko na ekranie --------
    pygame.display.update()
    zegar.tick(FPS)

pygame.quit()
quit()

