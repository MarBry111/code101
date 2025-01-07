# załadowanie bibliotek/pakietów
import pygame
import random

# inicjalizacja pygame
pygame.init()

# utworzenie zmiennych
# ze stałą wartoscią - nie zmienia sie w trakcie działania programu

# rozmiar segmentu węża oraz ile segmentów ma się zmieścić na ekranie
rozmiar_segmentu_weza = 60
ile_segmentow_w_ekranie = 10

# rozmiar ekranu np: (600, 600)
# oraz stworzenie obiektu ekranu
SCREEN_SIZE = (ile_segmentow_w_ekranie * rozmiar_segmentu_weza, ile_segmentow_w_ekranie * rozmiar_segmentu_weza)
screen = pygame.display.set_mode(SCREEN_SIZE)

# kolor węża (R, G, B)
kolor_weza = (0, 255, 0)

# zegar do odliczania FPSów
zegar = pygame.time.Clock()
FPS = 60

# zmienne ze zmienną wartoscią - zmienia sie w trakcie działania programu
# numer obecnej klatki (FPS = 60, zalem wartosci od 0 do 59)
klatka = 0

# pierwotne położenie głowy węża
x = [rozmiar_segmentu_weza]
y = [rozmiar_segmentu_weza]

# pierwotne położenie ziemniaka
x_ziemniak = 420
y_ziemniak = 300

# prędkości węża:
# vx - po osi x, prawo/lewo
# vy - po osi y, góra/dół
vx = rozmiar_segmentu_weza
vy = 0

# liczba punktów
punkty = 0

# informacja czy waż żyje
# True -> żyje, prawda że żyje
# -> False, nie żyje, nie prawda zę żyje
waz_zyje = True

# rodzaj fontu ktory bedziemy uzywac
font = pygame.font.Font(None, 74)

# główna pętla programu (sprawia że ekran się odświeża, wąż rusza itp)
while True:
    # pętla po eventach 
    for event in pygame.event.get():
        # jeśli zostanie wciśniety x -> zamknij program
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

        # jeśli wąż jest zielonego koloru
        if kolor_weza == (0, 255, 0):
            # jeśli event to KEYDOWN - naciśnięcie klawisza
            # oraz naciśniety klawisz to, odpowiednio UP (strzałka do góry), DOWN (do dołu) itp
            # to zmień prędkosći vx (lewo minusowe wratosci, prawo dodatnie, zero - wąż nie rusza się na boki)
            # oraz vy (góra minusowe wratosci, dół dodatnie, 0 - wąż nie rusza się góra dół)
            if event.type == pygame.KEYDOWN and event.key == pygame.K_UP:
                vx = 0
                vy = -rozmiar_segmentu_weza
            if event.type == pygame.KEYDOWN and event.key == pygame.K_DOWN:
                vx = 0
                vy = rozmiar_segmentu_weza
            if event.type == pygame.KEYDOWN and event.key == pygame.K_LEFT:
                vx = -rozmiar_segmentu_weza
                vy = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RIGHT:
                vx = rozmiar_segmentu_weza
                vy = 0
    
    # co krok w pętli zmień numer klatki
    # jeśli numer klatki równa się60 to wyzeruj licznik
    klatka = klatka + 1
    if klatka == 60:
        klatka = 0

    # co 20 klatke, czyli dla klatki 0, 20, 40
    # przesuń węża zgodnie z prędkością 
    if klatka in [0, 20, 40]:
        # załóż że nie dodajemy segmentu
        dodaj_segment = False
        # jeśli x i y węża równająsięx i y ziemniaka 
        # to wąż zjadł ziemniaka
        # i należy wygenerować nowe położenie ziemniaka (nadpisać wartości x i y ziemniaka)
        if x[0] == x_ziemniak and y[0] == y_ziemniak:
            punkty = punkty + 1
            print(punkty)
            x_ziemniak = random.randint(0, ile_segmentow_w_ekranie - 1) * 60
            y_ziemniak = random.randint(0, ile_segmentow_w_ekranie - 1) * 60

            # jeśli zjadł ziemniaka to chcemy dodać segment
            dodaj_segment = True

        # zapisz koniec wężą
        x_end = x[-1]
        y_end = y[-1]

        # przesuń węża na miejsce następnego segmentu
        if len(x) > 1:
            x[1:] = x[:-1]
            y[1:] = y[:-1]

        # przesuń głowę węża
        x[0] = x[0] + vx
        y[0] = y[0] + vy

        # jeśli dodaj segment jest ptrawdą to dodaj egment w miejscu stargeo ogona
        if dodaj_segment:
            x.append(x_end)
            y.append(y_end)

    # smierc/ przegrales
    # jeśli wąż poza planszą
    #  (x - sprawdź czy prawo lewo wyszłą głowa)
    #  (y - sprawdź czy góra dół wyszłą głowa)
    # to:
    if (
        x[0] < 0
        or x[0] > (ile_segmentow_w_ekranie - 1) * rozmiar_segmentu_weza
        or y[0] < 0
        or y[0] > (ile_segmentow_w_ekranie - 1) * rozmiar_segmentu_weza
    ):
        #  zmień kolor węża na czerwony
        kolor_weza = (255, 0, 0)
        # cofnij głowę o krok wstecz (żeby ją było widać na ekranie) 
        x[0] = x[0] - vx
        y[0] = y[0] - vy
        # ustaw vx i vy na 0 - żeby wąż się nie ruszał
        vx = 0
        vy = 0
        # ustal wartosć wąż żyje na fałsz
        waz_zyje = False

    # zapełnij cały ekrna kolorem czarnym
    #  R = 0
    #  G = 0
    #  B = 0
    # zatem brak koloru
    screen.fill((0, 0, 0))

    # jeśli wąż żyje
    if waz_zyje == True:
        # rusyj ziemniaka na ekranie
        pygame.draw.rect(
            screen,
            (255, 255, 255),
            (x_ziemniak, y_ziemniak, rozmiar_segmentu_weza, rozmiar_segmentu_weza),
        )
        # rysuj węża na ekranie (segment po segmencie)
        # rusyj węża po ziemniaku, wtedy wąż "zjada" ziemniaka
        for xi, yi in zip(x, y):
            pygame.draw.rect(screen, kolor_weza, (xi, yi, rozmiar_segmentu_weza, rozmiar_segmentu_weza))
        # stwórz obiek z liczbą punktów
        text = font.render(str(punkty), True, (255, 255, 255))
        # wyświetl na ekranie liczbę punktów
        screen.blit(text, (0, 0))
    else:
        # jeśli wąż nie żyje
        # stwórz obiek z napiszem umarłeś
        text_lose = font.render("UMARŁEŚ", True, (255, 0, 0))
        # wyświetl na ekranie napis umarłweś
        screen.blit(text_lose, (0, 0))

    # odśwież pygamea
    pygame.display.update()
    # pilnuj 60 FPSów
    zegar.tick(FPS)
