-- Tworzenie tabeli Osoby
CREATE TABLE IF NOT EXISTS Osoby (
    ID_Osoby INTEGER PRIMARY KEY AUTOINCREMENT,
    Imie TEXT NOT NULL,
    Nazwisko TEXT NOT NULL,
    Wiek INTEGER,
    Zawod TEXT,
    Cecha_Charakterystyczna TEXT
);

-- Tworzenie tabeli Miejsca
CREATE TABLE IF NOT EXISTS Miejsca (
    ID_Miejsca INTEGER PRIMARY KEY AUTOINCREMENT,
    Nazwa_Miejsca TEXT NOT NULL UNIQUE,
    Opis_Miejsca TEXT
);

-- Tworzenie tabeli Przedmioty
CREATE TABLE IF NOT EXISTS Przedmioty (
    ID_Przedmiotu INTEGER PRIMARY KEY AUTOINCREMENT,
    Nazwa_Przedmiotu TEXT NOT NULL,
    Opis_Przedmiotu TEXT,
    ID_Wlasciciela INTEGER,
    Miejsce_Znalezienia INTEGER,
    FOREIGN KEY (ID_Wlasciciela) REFERENCES Osoby(ID_Osoby),
    FOREIGN KEY (Miejsce_Znalezienia) REFERENCES Miejsca(ID_Miejsca)
);

-- Tworzenie tabeli Zeznania_Swiadkow
CREATE TABLE IF NOT EXISTS Zeznania_Swiadkow (
    ID_Zeznania INTEGER PRIMARY KEY AUTOINCREMENT,
    ID_Osoby_Zeznajacej INTEGER NOT NULL,
    Data_Zeznania DATE,
    Tresc_Zeznania TEXT NOT NULL,
    ID_Powiazanego_Miejsca INTEGER,
    ID_Powiazanej_Osoby INTEGER,
    FOREIGN KEY (ID_Osoby_Zeznajacej) REFERENCES Osoby(ID_Osoby),
    FOREIGN KEY (ID_Powiazanego_Miejsca) REFERENCES Miejsca(ID_Miejsca),
    FOREIGN KEY (ID_Powiazanej_Osoby) REFERENCES Osoby(ID_Osoby)
);