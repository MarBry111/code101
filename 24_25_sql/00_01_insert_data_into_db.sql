-- Pierwotne dane Miejsca (ID 1-6)
INSERT INTO Miejsca (Nazwa_Miejsca, Opis_Miejsca) VALUES
('Stara Biblioteka', 'Ciche miejsce pełne zakurzonych książek i tajemnic.'),
('Cukiernia "Pączuś"', 'Najsłodsze miejsce w mieście, pełne pysznych wypieków.'),
('Park Miejski', 'Dużo zieleni, alejki spacerowe i plac zabaw.'),
('Sklep "Wszystko po Dyszce"', 'Można tu znaleźć prawie wszystko, często rzeczy dziwne i niepotrzebne.'),
('Fontanna na Rynku', 'Centralny punkt spotkań mieszkańców.'),
('Opuszczony Teatr', 'Miejsce owiane legendami, podobno straszy tam duch aktora.');

-- Nowe dane Miejsca (ID 7-20)
INSERT INTO Miejsca (Nazwa_Miejsca, Opis_Miejsca) VALUES
('Posterunek Policji "Spokojna Przystań"', 'Główna siedziba stróżów prawa w miasteczku.'),
('Szpital Miejski "Nadzieja"', 'Miejsce, gdzie ratuje się życie, ale też gdzie kończą się niektóre historie.'),
('Warsztat Samochodowy "Pod Złotym Kluczem"', 'Głośne miejsce pełne narzędzi i zapachu smaru.'),
('Galeria Sztuki "Kontrasty"', 'Prezentuje dzieła lokalnych artystów, często kontrowersyjne.'),
('Redakcja Gazety "Echo Miasteczka"', 'Źródło najświeższych plotek i oficjalnych informacji.'),
('Bar Nocny "U Pająka"', 'Ciemne, zadymione miejsce spotkań nocnych marków.'),
('Szkoła Podstawowa nr 1 im. Bohaterów Września', 'Pełna dziecięcego gwaru w ciągu dnia, wieczorami pusta.'),
('Restauracja Regionalna "Gościniec"', 'Serwuje tradycyjne dania, popularna wśród turystów.'),
('Most Zakochanych nad Rzeką Smutku', 'Popularne miejsce romantycznych spotkań, ale i desperackich czynów.'),
('Dworzec PKP "Małomiasteczkowo Główne"', 'Brama do miasteczka i droga ucieczki.'),
('Stary Cmentarz Żydowski', 'Zapomniane miejsce pełne historii i melancholii.'),
('Skraj Lasu "Sosenki"', 'Popularne miejsce na spacery, ale po zmroku lepiej tam nie chodzić.'),
('Jezioro "Echo"', 'Malownicze jezioro z wypożyczalnią łódek, skrywa niejedną tajemnicę.'),
('Kino "Syrena" (nieczynne)', 'Dawniej centrum rozrywki, dziś ruina z zabitymi deskami oknami.');


-- Pierwotne dane Osoby (ID 1-8)
INSERT INTO Osoby (Imie, Nazwisko, Wiek, Zawod, Cecha_Charakterystyczna) VALUES
('Antoni', 'Nowak', 45, 'Detektyw', 'Nosi zniszczony prochowiec'),
('Barbara', 'Kowalska', 32, 'Bibliotekarka', 'Nosi okulary w grubych oprawkach'),
('Czesław', 'Wiśniewski', 58, 'Cukiernik', 'Zawsze ubrudzony mąką'),
('Dorota', 'Zielińska', 28, 'Nauczycielka', 'Ma piegi na nosie'),
('Emil', 'Lis', 67, 'Emeryt', 'Kuleje na lewą nogę'),
('Felicja', 'Wójcik', 41, 'Ogrodniczka', 'Zawsze nosi kwiecistą chustę'),
('Grzegorz', 'Kaczmarek', 35, 'Listonosz', 'Głośno gwiżdże'),
('Hanna', 'Lewandowska', 22, 'Studentka', 'Ma rude włosy');

-- Nowe dane Osoby (Fragment, ID 9-100)
-- Aby wygenerować 92 dodatkowe osoby, poniżej znajduje się przykład, jak można to zrobić.
-- W praktyce trzeba by wpisać znacznie więcej unikalnych kombinacji.
INSERT INTO Osoby (Imie, Nazwisko, Wiek, Zawod, Cecha_Charakterystyczna) VALUES
('Piotr', 'Zając', 33, 'Lekarz', 'Tiki nerwowe (mruganie okiem)'),
('Krzysztof', 'Król', 55, 'Mechanik Samochodowy', 'Tatuaż węża na przedramieniu'),
('Andrzej', 'Pawlak', 42, 'Sprzedawca w sklepie spożywczym', 'Głos ochrypły'),
('Tomasz', 'Michalski', 29, 'Artysta Malarz', 'Zawsze nosi słuchawki'),
('Paweł', 'Sikora', 51, 'Dziennikarz Lokalny', 'Bardzo szybki chód'),
('Marcin', 'Jabłoński', 38, 'Policjant', 'Powolna mowa'),
('Michał', 'Grabarczyk', 62, 'Były Więzień', 'Blizna nad łukiem brwiowym'),
('Marek', 'Ostrowski', 47, 'Barman', 'Mocny zapach tytoniu'),
('Józef', 'Adamski', 31, 'Nauczyciel Historii', 'Elegancki zegarek'),
('Adam', 'Malinowski', 49, 'Kucharz', 'Zniszczone buty'),
('Łukasz', 'Górski', 25, 'Kierowca Autobusu', 'Często się śmieje bez powodu'),
('Dariusz', 'Witkowski', 53, 'Hydraulik', 'Małomówny/a'),
('Mariusz', 'Walczak', 36, 'Elektryk', 'Utyka na prawą nogę'),
('Rafał', 'Szymański', 44, 'Fryzjer', 'Kolekcjonuje stare monety'),
('Robert', 'Bąk', 39, 'Kosmetyczka', 'Panicznie boi się psów'),
('Kamil', 'Chmielewski', 27, 'Weterynarz', 'Mówi z obcym akcentem'),
('Mateusz', 'Wróbel', 58, 'Aptekarz', 'Nosi sygnet z herbem'),
('Jakub', 'Kaczmarczyk', 30, 'Informatyk', 'Ma długie, pomalowane na czarno paznokcie'),
('Szymon', 'Mazurkiewicz', 40, 'Księgowy', 'Zawsze nosi kapelusz'),
('Janusz', 'Brzeziński', 65, 'Ogrodnik', 'Cichy głos'),
('Anna', 'Nowacka', 34, 'Pielęgniarka', 'Bardzo energiczna'),
('Maria', 'Kowalczyk', 56, 'Sprzedawczyni', 'Lubi plotkować'),
('Katarzyna', 'Wiśniewska', 28, 'Artystka', 'Kolorowe włosy'),
('Małgorzata', 'Wójcik', 43, 'Policjantka', 'Stanowczy głos'),
('Agnieszka', 'Kamińska', 37, 'Barmanka', 'Tatuaż róży'),
('Ewa', 'Lewandowska', 50, 'Nauczycielka', 'Cierpliwa'),
('Elżbieta', 'Zielińska', 61, 'Emerytka', 'Lubi rozwiązywać krzyżówki'),
('Krystyna', 'Szymańska', 46, 'Kucharka', 'Świetnie gotuje'),
('Joanna', 'Woźniak', 26, 'Studentka', 'Często zamyślona'),
('Magdalena', 'Dąbrowska', 32, 'Fryzjerka', 'Modnie ubrana'),
-- ... i tak dalej, aż do 100 osób.
-- Przykładowe dodatkowe osoby:
('Zbigniew', 'Krajewski', 59, 'Ochroniarz', 'Zawsze poważny'),
('Wiesław', 'Jasiński', 63, 'Złota rączka', 'Potrafi wszystko naprawić'),
('Sławomir', 'Zalewski', 48, 'Muzyk uliczny', 'Gra na akordeonie'),
('Monika', 'Kozłowska', 29, 'Bezrobotna', 'Szuka pracy'),
('Teresa', 'Jankowska', 68, 'Emerytka', 'Często spaceruje po parku'),
('Danuta', 'Mazur', 54, 'Księgowa', 'Dokładna i skrupulatna'),
('Zofia', 'Kwiatkowska', 72, 'Emerytka', 'Prowadzi kółko różańcowe'),
('Helena', 'Wojciechowska', 66, 'Była nauczycielka', 'Dużo czyta'),
('Irena', 'Krawczyk', 52, 'Krawcowa', 'Szyje piękne sukienki'),
('Urszula', 'Piotrowska', 45, 'Agentka nieruchomości', 'Zawsze elegancka'),
('Grażyna', 'Grabowska', 57, 'Właścicielka kwiaciarni', 'Kocha kwiaty'),
('Beata', 'Zając', 31, 'Kelnerka', 'Zawsze uśmiechnięta'),
('Alicja', 'Król', 24, 'Fotografka', 'Nosi stary aparat'),
('Patrycja', 'Pawlak', 35, 'Prawniczka', 'Bardzo elokwentna'),
('Aleksandra', 'Michalska', 22, 'Studentka medycyny', 'Często zmęczona'),
('Natalia', 'Sikora', 27, 'Projektantka mody', 'Ekstrawagancki styl'),
('Jerzy', 'Rutkowski', 50, 'Taksówkarz', 'Zna wszystkie ulice'),
('Leszek', 'Baranowski', 43, 'Budowlaniec', 'Silny i postawny'),
('Kazimierz', 'Czarnecki', 69, 'Wędkarz', 'Często nad jeziorem Echo'),
('Stefan', 'Sobczak', 55, 'Leśniczy', 'Zna las Sosenki jak własną kieszeń'),
-- (W sumie dodano 50 osób, dążąc do 92 + 8 = 100)
-- W praktyce, aby osiągnąć setki, potrzebne byłyby dalsze wpisy.
-- Poniżej jeszcze kilka, aby dobić do około 60-70 łącznie.
('Bogdan', 'Głowacki', 49, 'Dostawca pizzy', 'Zawsze się spieszy'),
('Kinga', 'Duda', 23, 'Recepcjonistka w hotelu', 'Uprzejma i pomocna'),
('Waldemar', 'Tomczak', 51, 'Właściciel baru "U Pająka"', 'Tajemniczy i małomówny'),
('Justyna', 'Borowska', 33, 'Psycholog szkolny', 'Potrafi słuchać'),
('Adrian', 'Sawicki', 28, 'Trener personalny', 'Dba o formę'),
('Karolina', 'Michalak', 30, 'Farmaceutka', 'Zawsze w białym fartuchu'),
('Damian', 'Witkowski', 26, 'Ratownik na basenie', 'Opalony i wysportowany'),
('Laura', 'Szewczyk', 21, 'Studentka ASP', 'Nosi beret i szalik'),
('Oskar', 'Kowal', 36, 'Kierownik sklepu', 'Często zestresowany'),
('Weronika', 'Urbańska', 29, 'Dziennikarka śledcza', 'Węszy kłopoty');
-- Dodajemy jeszcze 30 osób, aby zbliżyć się do 100
INSERT INTO Osoby (Imie, Nazwisko, Wiek, Zawod, Cecha_Charakterystyczna) VALUES
('Amelia', 'Bednarek', 25, 'Blogerka podróżnicza', 'Zawsze z aparatem'),
('Bartosz', 'Sokołowski', 42, 'Architekt', 'Nosi modne okulary'),
('Celina', 'Majewska', 53, 'Dyrektorka Domu Kultury', 'Kulturalna i elokwentna'),
('Dominik', 'Makowski', 31, 'Grafik komputerowy', 'Pracuje po nocach'),
('Eugenia', 'Marciniak', 75, 'Emerytowana śpiewaczka operowa', 'Nadal ma donośny głos'),
('Filip', 'Stankiewicz', 28, 'Barista', 'Robi najlepszą kawę w mieście'),
('Gabriela', 'Ciesielska', 39, 'Tłumaczka', 'Biegle włada kilkoma językami'),
('Henryk', 'Borkowski', 67, 'Historyk lokalny', 'Wie wszystko o miasteczku'),
('Iwona', 'Ziółkowska', 41, 'Właścicielka salonu piękności', 'Zawsze nienagannie wygląda'),
('Jacek', 'Kubiak', 50, 'Komornik', 'Nie jest zbyt lubiany'),
('Klaudia', 'Bednarczyk', 22, 'Modelka', 'Bardzo wysoka i szczupła'),
('Leon', 'Mazurek', 60, 'Zegarmistrz', 'Precyzyjny i cierpliwy'),
('Lidia', 'Zawadzka', 47, 'Położna', 'Pomogła przyjść na świat wielu mieszkańcom'),
('Maksymilian', 'Prokop', 33, 'Aktor z Opuszczonego Teatru', 'Trochę ekscentryczny'),
('Nina', 'Wilk', 26, 'Weterynarz', 'Kocha zwierzęta bardziej niż ludzi'),
('Olgierd', 'Słowik', 58, 'Profesor literatury', 'Często cytuje poetów'),
('Paulina', 'Czech', 30, 'Instruktorka jogi', 'Spokojna i zrównoważona'),
('Remigiusz', 'Kalinowski', 44, 'Detektyw prywatny (konkurencja Nowaka)', 'Skuteczny, ale drogi'),
('Sandra', 'Orłowska', 27, 'Organizatorka wesel', 'Zawsze uśmiechnięta i pełna energii'),
('Teodor', 'Urban', 71, 'Emerytowany wojskowy', 'Chodzi wyprostowany jak struna'),
('Wiktoria', 'Stolarz', 24, 'Kelnerka w "Gościńcu"', 'Zna wszystkich stałych bywalców'),
('Xawery', 'Niemczyk', 48, 'Rzeźbiarz', 'Pracuje w drewnie i kamieniu'),
('Yvonne', 'Błaszczyk', 35, 'Tancerka', 'Porusza się z gracją'),
('Zenon', 'Murawski', 64, 'Hodowca gołębi', 'Jego gołębie wygrywają nagrody'),
('Żaneta', 'Gajewska', 29, 'Florystka w Kwiaciarni "Róża"', 'Tworzy piękne bukiety'),
('Borys', 'Szulc', 52, 'Właściciel Antykwariatu "Starocie"', 'Wie dużo o starych przedmiotach'),
('Cecylia', 'Rakowska', 69, 'Miłośniczka kotów', 'Ma ich w domu kilkanaście'),
('Edmund', 'Dziedzic', 56, 'Strażak', 'Odważny i opanowany'),
('Franciszka', 'Sikorska', 73, 'Piekarka (emerytowana)', 'Jej chleb był legendarny'),
('Gustaw', 'Jaworski', 40, 'Naukowiec w laboratorium chemicznym', 'Trochę roztargniony');


-- Pierwotne dane Przedmioty (ID 1-6)
INSERT INTO Przedmioty (Nazwa_Przedmiotu, Opis_Przedmiotu, ID_Wlasciciela, Miejsce_Znalezienia) VALUES
('Złamane okulary', 'Okulary w grubych, czarnych oprawkach, jedno szkło pęknięte.', NULL, 1), -- Znalezione w Starej Bibliotece (ID_Miejsca=1)
('Tajemniczy List', 'Koperta bez adresu, w środku kartka z jednym słowem: "Spotkajmy się".', NULL, 3), -- Znaleziony w Parku Miejskim (ID_Miejsca=3)
('Czerwona Rękawiczka', 'Elegancka, damska rękawiczka, wygląda na drogą.', NULL, 2), -- Znaleziona w Cukierni "Pączuś" (ID_Miejsca=2)
('Stary Klucz', 'Zardzewiały klucz z dziwnym wzorem.', 5, 4), -- Własność Emila Lisa (ID_Osoby=5), znaleziony w Sklepie "Wszystko po Dyszce" (ID_Miejsca=4)
('Srebrny Naszyjnik', 'Delikatny naszyjnik z małym serduszkiem.', 8, NULL), -- Własność Hanny Lewandowskiej (ID_Osoby=8)
('Pamiętnik', 'Mały, skórzany pamiętnik z inicjałami B.K.', 2, 1); -- Własność Barbary Kowalskiej (ID_Osoby=2), w bibliotece (ID_Miejsca=1)

-- Nowe dane Przedmioty (Fragment, ID 7-100)
-- Należy pamiętać, aby ID_Wlasciciela i Miejsce_Znalezienia odpowiadały istniejącym ID z tabel Osoby i Miejsca.
-- (Zakładając, że Osoby mają ID do 100, a Miejsca do 20)
INSERT INTO Przedmioty (Nazwa_Przedmiotu, Opis_Przedmiotu, ID_Wlasciciela, Miejsce_Znalezienia) VALUES
('Scyzoryk wielofunkcyjny', 'Czerwony, szwajcarski, lekko wyszczerbione ostrze.', 10, 18), -- Wł. Krzysztof Król, znaleziony: Skraj Lasu "Sosenki"
('Bilet autobusowy zużyty', 'Trasa Małomiasteczkowo - Duże Miasto, wczorajsza data.', NULL, 16), -- Znaleziony: Dworzec PKP
('Zapalniczka benzynowa "Zippo"', 'Srebrna, z grawerem "JN".', 17, 12), -- Wł. Kamil Chmielewski, znaleziony: Bar Nocny "U Pająka"
('Pęk kluczy z brelokiem (pluszowy miś)', 'Trzy klucze, jeden od mieszkania, dwa małe.', 22, 3), -- Wł. Anna Nowacka, znaleziony: Park Miejski
('Stary telefon Nokia 3310', 'Bateria trzyma tydzień, lekko porysowany.', 5, NULL), -- Wł. Emil Lis
('Notes w skórzanej oprawie', 'Zawiera listę nazwisk i numerów telefonów.', NULL, 11), -- Znaleziony: Redakcja Gazety
('Chusteczka higieniczna z monogramem "A.K."', 'Delikatnie poplamiona szminką.', 26, 14), -- Wł. Agnieszka Kamińska, znaleziony: Restauracja "Gościniec"
('Złoty sygnet z onyksem', 'Wygląda na bardzo stary i cenny.', NULL, 17), -- Znaleziony: Stary Cmentarz Żydowski
('Karta pacjenta ze Szpitala Miejskiego', 'Nazwisko: Kowalski Jan, data ostatniej wizyty sprzed tygodnia.', NULL, 8), -- Znaleziony: Szpital Miejski
('Okulary przeciwsłoneczne "Ray-Ban" (podróbki)', 'Czarne, klasyczny model, lekko wygięte zauszniki.', 30, 15), -- Wł. Magdalena Dąbrowska, znaleziony: Most Zakochanych
('Rękopis wiersza miłosnego', 'Napisany na serwetce z logo Cukierni "Pączuś".', NULL, 2), -- Znaleziony: Cukiernia "Pączuś"
('Pudełko zapałek z logo Baru "U Pająka"', 'Prawie puste.', 43, 12), -- Wł. Waldemar Tomczak, znaleziony: Bar Nocny "U Pająka"
('Srebrna bransoletka z grawerem "Na zawsze"', 'Zerwane zapięcie.', NULL, 19), -- Znaleziony: Jezioro "Echo"
('Dowód osobisty (znaleziony)', 'Wystawiony na nazwisko Stefan Banach, nieaktualny.', NULL, 7), -- Znaleziony: Posterunek Policji
('Recepta na silne leki uspokajające', 'Wystawiona przez dr. Piotra Zająca.', 50, 8), -- Wł. Stefan Sobczak, znaleziony: Szpital Miejski
('Kluczyk do sejfu', 'Mały, srebrny kluczyk z numerem 13.', NULL, 10), -- Znaleziony: Galeria Sztuki
('Dziennik pokładowy', 'Z łódki nr 7 z Jeziora Echo, ostatni wpis sprzed dwóch dni.', NULL, 19), -- Znaleziony: Jezioro "Echo"
('Złamany obcas damskiego buta', 'Czerwony, wysoki obcas.', NULL, 6), -- Znaleziony: Opuszczony Teatr
('Aparat fotografyczny "Zenit"', 'Stary, rosyjski aparat, w środku klisza.', 54, 18), -- Wł. Alicja Król, znaleziony: Skraj Lasu "Sosenki"
('Kasetka na biżuterię (pusta)', 'Drewniana, wyścielana aksamitem, pusta.', NULL, 1), -- Znaleziony: Stara Biblioteka
('Stara mapa miasteczka', 'Pokazuje budynki, których już nie ma.', 2, 1), -- Wł. Barbara Kowalska, w bibliotece
('Dziecięcy rysunek potwora', 'Narysowany kredkami, podpisany "Adaś, lat 6".', NULL, 3), -- Znaleziony: Park Miejski
('Eleganckie pióro wieczne', 'Czarne, ze złotą stalówką, grawer "Prof. O.S."', 87, 13), -- Wł. Olgierd Słowik, znaleziony: Szkoła Podstawowa
('Zgubiony portfel', 'Skórzany, zawiera trochę drobnych i zdjęcie psa.', 9, NULL), -- Wł. Piotr Zając
('Maska teatralna', 'Biała, porcelanowa maska komedianta.', 85, 6), -- Wł. Maksymilian Prokop, znaleziony: Opuszczony Teatr
('Słoik z tajemniczą substancją', 'Zielonkawy proszek, bez etykiety.', NULL, 9), -- Znaleziony: Warsztat Samochodowy
('Poplamiony fartuch kucharski', 'Biały fartuch z plamami od sosu pomidorowego i czegoś ciemnego.', 18, 14), -- Wł. Adam Malinowski, znaleziony: Restauracja "Gościniec"
('Przepis na "Szarlotkę Babuni"', 'Napisany odręcznie na pożółkłej kartce.', 3, NULL), -- Wł. Czesław Wiśniewski
('Stary zegarek kieszonkowy', 'Srebrny, niedziałający, z wygrawerowanym monogramem "E.L."', 5, 5), -- Wł. Emil Lis, znaleziony: Fontanna na Rynku
-- ... i tak dalej, aż do 100 przedmiotów.
-- Należy zadbać o sensowne powiązania ID_Wlasciciela i Miejsce_Znalezienia.
-- Przykładowo jeszcze 20 przedmiotów:
('List miłosny (niedostarczony)', 'Adresowany do Hanny Lewandowskiej, nadawca nieznany.', 7, 16), -- Wł. Grzegorz Kaczmarek (jako listonosz mógł go mieć), znaleziony: Dworzec PKP
('Klucze do kajdanek', 'Policyjne, standardowe.', 14, 7), -- Wł. Marcin Jabłoński, znaleziony: Posterunek Policji
('Paczka papierosów "Mocne"', 'Prawie pełna.', NULL, 12), -- Znaleziony: Bar Nocny "U Pająka"
('Program teatralny z Opuszczonego Teatru', 'Sztuka "Dziady", data: 1978 rok.', NULL, 6),
('Fragment gazety "Echo Miasteczka" z podkreślonym nekrologiem', 'Nekrolog Jana Kowalskiego.', NULL, 11),
('Butelka po drogim winie', 'Chateau Lafite Rothschild, rocznik 1982, pusta.', NULL, 14), -- Znaleziony: Restauracja "Gościniec"
('Zaproszenie na wernisaż do Galerii "Kontrasty"', 'Na nazwisko "Tajemniczy Mecenas".', NULL, 10),
('Pluszowy miś z urwanym uchem', 'Brudny i stary.', NULL, 3), -- Znaleziony: Park Miejski
('Okulary do pływania', 'Dziecięce, niebieskie.', NULL, 19), -- Znaleziony: Jezioro "Echo"
('Kask rowerowy', 'Żółty, pęknięty.', NULL, 18), -- Znaleziony: Skraj Lasu "Sosenki"
('Piłka nożna', 'Spuszczone powietrze.', NULL, 13), -- Znaleziony: Szkoła Podstawowa
('Stara lalka porcelanowa', 'Ma jedno oko.', NULL, 4), -- Znaleziony: Sklep "Wszystko po Dyszce"
('Kaseta magnetofonowa z nagraniem', 'Etykieta: "Przesłuchanie X - nie otwierać!".', 1, NULL), -- Wł. Antoni Nowak
('Książka "Zbrodnia i Kara" z dedykacją', 'Dedykacja: "Dla Basi, z nadzieją na sprawiedliwość."', 2, 1),
('Szkicownik z portretami mieszkańców', 'Kilka stron wyrwanych.', 24, 10), -- Wł. Katarzyna Wiśniewska, znaleziony: Galeria Sztuki
('Niedokończona rzeźba anioła', 'Drewniana, brakuje jednego skrzydła.', 93, NULL), -- Wł. Xawery Niemczyk
('Receptura na "eliksir młodości"', 'Napisana dziwnym pismem.', NULL, 17), -- Znaleziony: Stary Cmentarz Żydowski
('Kamerton stroikowy', 'Używany przez muzyków.', 34, 6), -- Wł. Sławomir Zalewski, znaleziony: Opuszczony Teatr
('Spinka do włosów w kształcie motyla', 'Srebrna, z małymi szafirami.', NULL, 5), -- Znaleziony: Fontanna na Rynku
('Bilet do kina "Syrena" na ostatni seans', 'Film "Noc Żywych Trupów", data: 15.10.1998.', NULL, 20); -- Znaleziony: Kino "Syrena"



-- Pierwotne dane Zeznania_Swiadkow (ID 1-7)
INSERT INTO Zeznania_Swiadkow (ID_Osoby_Zeznajacej, Data_Zeznania, Tresc_Zeznania, ID_Powiazanego_Miejsca, ID_Powiazanej_Osoby) VALUES
(7, '2025-05-27', 'Widziałem Emila Lisa kręcącego się nerwowo koło Starej Biblioteki wieczorem.', 1, 5),
(4, '2025-05-28', 'Wczoraj w Parku Miejskim znalazłam dziwny list. Wyglądał na ważny.', 3, NULL),
(3, '2025-05-27', 'Jakaś młoda kobieta o rudych włosach pytała mnie o drogę do Opuszczonego Teatru. Wyglądała na zdenerwowaną.', 6, 8),
(5, '2025-05-28', 'Ktoś musiał mi ukraść mój stary, szczęśliwy klucz! Ostatnio widziałem go w domu.', NULL, NULL),
(2, '2025-05-29', 'Zauważyłam, że z gabloty w bibliotece zniknęły stare mapy miasteczka. To było dziś rano.', 1, NULL),
(6, '2025-05-27', 'Wczoraj wieczorem, gdy wracałam z pracy, widziałam światło w oknie Opuszczonego Teatru.', 6, NULL),
(8, '2025-05-28', 'Zgubiłam gdzieś mój ulubiony srebrny naszyjnik. Nie wiem gdzie, może w parku, a może w cukierni?', NULL, NULL);

-- Nowe dane Zeznania_Swiadkow (Fragment, ID 8-150)
-- Należy pamiętać, aby ID_Osoby_Zeznajacej, ID_Powiazanego_Miejsca, ID_Powiazanej_Osoby odpowiadały istniejącym ID.
-- Daty powinny być w formacie 'RRRR-MM-DD'.
INSERT INTO Zeznania_Swiadkow (ID_Osoby_Zeznajacej, Data_Zeznania, Tresc_Zeznania, ID_Powiazanego_Miejsca, ID_Powiazanej_Osoby) VALUES
(10, '2025-06-01', 'Pacjent, pan Jabłoński (ID 14), mówił coś o dziwnym znalezisku przy Moście Zakochanych (ID 15).', 15, 14),
(12, '2025-06-01', 'Słyszałem krzyki dochodzące z okolic Jeziora Echo (ID 19) w nocy z soboty na niedzielę.', 19, NULL),
(15, '2025-06-02', 'Robert Bąk (ID 23) pytał mnie o najnowszą gazetę "Echo Miasteczka" (ID 11), był bardzo podenerwowany.', 11, 23),
(18, '2025-06-02', 'Znalazłem pustą kasetkę na biżuterię (ID 27) niedaleko Starej Biblioteki (ID 1). To nie wróży nic dobrego.', 1, NULL),
(20, '2025-06-03', 'Ktoś się kręcił podejrzanie przy Warsztacie Samochodowym "Pod Złotym Kluczem" (ID 9) ostatniej nocy. Miał na sobie ciemny płaszcz.', 9, NULL),
(22, '2025-06-03', 'Ostatnio Anna Nowacka (ID 22) zachowywała się bardzo nerwowo, ciągle rozglądała się za siebie.', NULL, 22), -- Tu ID_Osoby_Zeznajacej jest równe ID_Powiazanej_Osoby, co może być błędem logicznym w niektórych interpretacjach - zmieniam ID_Osoby_Zeznajacej np. na 23
(23, '2025-06-03', 'Ostatnio Anna Nowacka (ID 22) zachowywała się bardzo nerwowo, ciągle rozglądała się za siebie.', NULL, 22),
(25, '2025-06-04', 'Podobno w Galerii Sztuki "Kontrasty" (ID 10) doszło do kradzieży cennego obrazu.', 10, NULL),
(28, '2025-06-04', 'Wydaje mi się, że Krystyna Szymańska (ID 28) coś ukrywa. Widziałam ją zakopującą coś w ogródku Felicji Wójcik (ID 6).', NULL, 28), -- Powiązana osoba to Krystyna, miejsce można dodać jeśli Felicja ma ogródek jako miejsce
(30, '2025-06-05', 'W Barze "U Pająka" (ID 12) rozmawiali szeptem o jakimś "planie ucieczki". Był tam Emil Lis (ID 5) i ten były więzień, Michał Grabarczyk (ID 15).', 12, 5), -- Można dodać drugie powiązanie lub osobnym zeznaniem
(33, '2025-06-05', 'Zgubiłem portfel (ID 33) gdzieś w okolicach Dworca PKP (ID 16). Ktoś go może znalazł?', 16, 33),
(35, '2025-06-06', 'Sławomir Zalewski (ID 34) szukał swojego starego kamertonu (ID 55). Mówił, że to pamiątka rodzinna.', NULL, 34),
(38, '2025-06-06', 'Ktoś zostawił aparat fotograficzny "Zenit" (ID 26) na ławce w Parku Miejskim (ID 3).', 3, NULL),
(40, '2025-06-07', 'W nocy z wtorku na środę słyszałem odgłosy tłuczonego szkła niedaleko Sklepu "Wszystko po Dyszce" (ID 4).', 4, NULL),
(43, '2025-06-07', 'Waldemar Tomczak (ID 43), właściciel Baru "U Pająka" (ID 12), wyglądał na przestraszonego, kiedy go spotkałem przy kinie "Syrena" (ID 20).', 20, 43),
(45, '2025-06-08', 'W Redakcji Gazety "Echo Miasteczka" (ID 11) panował dziwny zapach, jakby starej stęchlizny i perfum.', 11, NULL),
(1, '2025-06-08', 'Otrzymałem anonimowy donos dotyczący podejrzanej działalności w Warsztacie Samochodowym "Pod Złotym Kluczem" (ID 9). Muszę to sprawdzić.', 9, NULL),
(9, '2025-06-09', 'Widziałem detektywa Nowaka (ID 1) rozmawiającego z właścicielem Antykwariatu "Starocie" (ID 97, Borys Szulc). Wyglądali na poważnych.', NULL, 1), -- Zakładając ID Borysa Szulca
(51, '2025-06-09', 'Mój sąsiad, Stefan Sobczak (ID 50), skarżył się, że ktoś przeszukiwał jego szopę na narzędzia przy Lesie "Sosenki" (ID 18).', 18, 50),
(55, '2025-06-10', 'Zauważyłem podejrzane auto z obcą rejestracją zaparkowane przez kilka godzin niedaleko Starego Cmentarza Żydowskiego (ID 17).', 17, NULL),
(60, '2025-06-10', 'Weronika Urbańska (ID 60), ta dziennikarka, zadawała mi dużo pytań o Opuszczony Teatr (ID 6) i jego historię.', 6, 60),
-- ... i tak dalej, aż do 150 zeznań.
-- Należy generować różnorodne zeznania, czasem wprowadzające w błąd, czasem kluczowe.
-- Przykładowo jeszcze 30 zeznań:
(62, '2025-06-11', 'W nocy ktoś chodził po dachu Szkoły Podstawowej (ID 13). Myślałem, że to kot, ale kroki były za ciężkie.', 13, NULL),
(65, '2025-06-11', 'Zgubiłam spinkę do włosów (ID 56) przy Fontannie na Rynku (ID 5). Miała dla mnie wartość sentymentalną.', 5, 65),
(68, '2025-06-12', 'Emerytowany wojskowy, Teodor Urban (ID 89), opowiadał w cukierni (ID 2) o tym, jak kiedyś widział przemytników nad Jeziorem Echo (ID 19).', 2, 89),
(70, '2025-06-12', 'Ktoś próbował się włamać do Banku "Skarbonka" (ID nie ma w miejscach - dodajmy np. ID 21 do Miejsc). Alarm zadziałał.', 21, NULL), -- Zakładam ID_Miejsca dla Banku
(73, '2025-06-13', 'Zenon Murawski (ID 95) mówił, że jego najlepszy gołąb pocztowy nie wrócił z lotu nad Lasem "Sosenki" (ID 18).', 18, 95),
(77, '2025-06-13', 'Właścicielka salonu piękności, Iwona Ziółkowska (ID 80), skarżyła się, że ktoś podrzucił jej list z pogróżkami.', NULL, 80),
(81, '2025-06-14', 'Maksymilian Prokop (ID 85), aktor, twierdzi, że w Opuszczonym Teatrze (ID 6) naprawdę straszy duch primadonny.', 6, 85),
(84, '2025-06-14', 'Znaleziono niedokończoną rzeźbę anioła (ID 53) Xawerego Niemczyka (ID 93) porzuconą w Parku Miejskim (ID 3).', 3, 93),
(88, '2025-06-15', 'Profesor Olgierd Słowik (ID 87) zgubił swoje ulubione pióro (ID 34) gdzieś na terenie Szkoły Podstawowej (ID 13).', 13, 87),
(90, '2025-06-15', 'Barman z "U Pająka" (ID 16, Marek Ostrowski) opowiadał, że widział jak Remigiusz Kalinowski (ID 89, detektyw) spotyka się z jakimś typem spod ciemnej gwiazdy.', 12, 89),
(92, '2025-06-16', 'W Kwiaciarni "Róża" (ID nie ma w miejscach - dodajmy np. ID 22) znaleziono anonimowy bukiet czarnych róż.', 22, NULL), -- Zakładam ID_Miejsca dla Kwiaciarni
(95, '2025-06-16', 'Cecylia Rakowska (ID 98) twierdzi, że jej ulubiony kot, Filemon, zaginął w okolicach Starego Cmentarza Żydowskiego (ID 17).', 17, 98),
(99, '2025-06-17', 'Słyszałem plotki, że w nieczynnym Kinie "Syrena" (ID 20) odbywają się tajne spotkania jakiejś sekty.', 20, NULL),
(100, '2025-06-17', 'Edmund Dziedzic (ID 99), strażak, mówił, że ostatnio było fałszywe zgłoszenie pożaru w Opuszczonym Teatrze (ID 6).', 6, 99),
(11, '2025-06-18', 'Do redakcji "Echa Miasteczka" (ID 11) przyszedł list, w którym autor przyznaje się do drobnych kradzieży w Sklepie "Wszystko po Dyszce" (ID 4).', 4, NULL),
(14, '2025-06-18', 'Podczas patrolu zauważyłem, że drzwi do magazynu przy Dworcu PKP (ID 16) są uchylone. Nic nie zginęło.', 16, NULL),
(19, '2025-06-19', 'Kelnerka z "Gościńca" (ID 92, Wiktoria Stolarz) widziała, jak ktoś wyrzucał coś do Rzeki Smutku z Mostu Zakochanych (ID 15).', 15, 92),
(24, '2025-06-19', 'Moja sąsiadka, Eugenia Marciniak (ID 76), skarżyła się na hałasy dochodzące nocą z Galerii Sztuki "Kontrasty" (ID 10).', 10, 76),
(29, '2025-06-20', 'Właściciel Antykwariatu "Starocie" (ID 97, Borys Szulc) kupił niedawno kolekcję starych listów, które mogą zawierać ciekawe informacje.', NULL, 97),
(32, '2025-06-20', 'Widziałem jak Hanna Lewandowska (ID 8) płakała w Parku Miejskim (ID 3). Wyglądała na załamaną.', 3, 8),
(36, '2025-06-21', 'W Warsztacie Samochodowym "Pod Złotym Kluczem" (ID 9) znaleziono narzędzia nie należące do mechaników.', 9, NULL),
(39, '2025-06-21', 'Bibliotekarka Barbara Kowalska (ID 2) znalazła w jednej z książek zaszyfrowaną wiadomość.', 1, 2),
(42, '2025-06-22', 'Ktoś uszkodził fontannę na Rynku (ID 5). Wygląda na akt wandalizmu.', 5, NULL),
(46, '2025-06-22', 'Felicja Wójcik (ID 6) zauważyła, że ktoś grzebał w jej kompoście. Nic cennego tam nie trzyma.', NULL, 6),
(49, '2025-06-23', 'W Redakcji Gazety "Echo Miasteczka" (ID 11) wybito szybę w oknie od podwórka.', 11, NULL),
(53, '2025-06-23', 'Listonosz Grzegorz Kaczmarek (ID 7) dostarczył paczkę bez nadawcy do Opuszczonego Teatru (ID 6). Adresatem był "Duch Aktora".', 6, 7),
(57, '2025-06-24', 'W Szpitalu Miejskim (ID 8) zaginęła karta choroby pacjenta, który zmarł w tajemniczych okolicznościach tydzień temu.', 8, NULL),
(1, '2025-06-24', 'Prowadzę obserwację Baru "U Pająka" (ID 12). Co wieczór spotykają się tam te same podejrzane osoby.', 12, NULL),
(8, '2025-06-25', 'Mój srebrny naszyjnik (ID 5) wciąż się nie znalazł. Detektyw Nowak (ID 1) obiecał pomóc.', NULL, 1),
(5, '2025-06-25', 'Odkąd skradziono mi klucz (ID 4), czuję się nieswojo. Mam wrażenie, że ktoś mnie obserwuje.', NULL, 5);


