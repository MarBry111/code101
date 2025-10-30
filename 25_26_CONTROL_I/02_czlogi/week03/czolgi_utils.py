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
V_POCISKU = 2

class Czolg:
    def __init__(self, x, y, sciezka_do_obrazka, player):
        self.x = x
        self.y = y
        self.obrazek = pygame.image.load(sciezka_do_obrazka)
        self.obrazek = pygame.transform.scale(self.obrazek, (ROZMIAR, ROZMIAR))
        self.obrazek_do_rysowania = self.obrazek.copy()
        self.player = player
        self.zycia = 3
        self.kierunek = "U" # Up Down Right Left
        self.hitbox = pygame.Rect(self.x, self.y, ROZMIAR, ROZMIAR)

    def rysuj(self, ekran):
        ekran.blit(self.obrazek_do_rysowania, (self.x, self.y))

    def update_hitbox(self):
        self.hitbox = pygame.Rect(self.x, self.y, ROZMIAR, ROZMIAR)

    def strzel(self):
        if self.kierunek == "U":
            p = Pocisk(self.x + ROZMIAR//2 - 5, self.y-40, 0, -V_POCISKU, self.player, self.kierunek)
        elif self.kierunek == "D":
            p = Pocisk(self.x + ROZMIAR//2 - 5, self.y + ROZMIAR + 10, 0, V_POCISKU, self.player, self.kierunek)
        elif self.kierunek == "R":
            p = Pocisk(self.x + ROZMIAR + 10, self.y + ROZMIAR//2 - 5, V_POCISKU, 0, self.player, self.kierunek)
        else:
            p = Pocisk(self.x - 40, self.y + ROZMIAR//2 - 5, -V_POCISKU, 0, self.player, self.kierunek)
        return p

    def obrot(self, event):
        if self.player == 1:
            if event.key == pygame.K_a:
                self.obrazek_do_rysowania = pygame.transform.rotate(self.obrazek, 90)
                self.kierunek = "L"
            elif event.key == pygame.K_d:
                self.obrazek_do_rysowania = pygame.transform.rotate(self.obrazek, -90)
                self.kierunek = "R"
            elif event.key == pygame.K_w:
                self.obrazek_do_rysowania = pygame.transform.rotate(self.obrazek, 0)
                self.kierunek = "U"
            elif event.key == pygame.K_s:
                self.obrazek_do_rysowania = pygame.transform.rotate(self.obrazek, 180)
                self.kierunek = "D"
        elif self.player == 2:
            if event.key == pygame.K_LEFT:
                self.obrazek_do_rysowania = pygame.transform.rotate(self.obrazek, 90)
                self.kierunek = "L"
            elif event.key == pygame.K_RIGHT:
                self.obrazek_do_rysowania = pygame.transform.rotate(self.obrazek, -90)
                self.kierunek = "R"
            elif event.key == pygame.K_UP:
                self.obrazek_do_rysowania = pygame.transform.rotate(self.obrazek, 0)
                self.kierunek = "U"
            elif event.key == pygame.K_DOWN:
                self.obrazek_do_rysowania = pygame.transform.rotate(self.obrazek, 180)
                self.kierunek = "D"

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

        self.update_hitbox()

class Pocisk:
    def __init__(self, x, y, vx, vy, player, kierunek):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.player = player
        self.obrazek = pygame.Surface((40, 10))
        self.obrazek.fill(CZERWONY)
        self.kierunek = kierunek
        self.hitbox = pygame.Rect(self.x, self.y, 40, 10)
        if kierunek == "U":
            self.obrazek = pygame.transform.rotate(self.obrazek, -90)
            self.hitbox = pygame.Rect(self.x, self.y, 10, 40)
        elif kierunek == "D":
            self.obrazek = pygame.transform.rotate(self.obrazek, 90)
            self.hitbox = pygame.Rect(self.x, self.y, 10, 40)
        elif kierunek == "R":
            self.obrazek = pygame.transform.rotate(self.obrazek, 0)

    def rysuj(self, ekran):
        ekran.blit(self.obrazek, (self.x, self.y))

    def ruszaj(self):
        self.x = self.x + self.vx
        self.y = self.y + self.vy
        self.update_hitbox()

    def update_hitbox(self):
        if self.kierunek in ["U", "D"]:
            self.hitbox = pygame.Rect(self.x, self.y, 10, 40)
        else:
            self.hitbox = pygame.Rect(self.x, self.y, 40, 10)