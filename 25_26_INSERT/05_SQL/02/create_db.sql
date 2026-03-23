-- ============================================================
--  AKADEMIA TRENERÓW POKÉMONÓW — baza danych do nauki SQL
-- ============================================================

CREATE TABLE trenerzy (
    id      INTEGER PRIMARY KEY,
    imie    TEXT    NOT NULL,
    wiek    INTEGER,
    miasto  TEXT,
    odznaki INTEGER   -- ile odznak zdobyli
);

CREATE TABLE pokemony (
    id         INTEGER PRIMARY KEY,
    nazwa      TEXT    NOT NULL,
    typ        TEXT,      -- Ogień, Woda, Trawa, Elektryczny, Psychiczny, Lodowy
    hp         INTEGER,
    atak       INTEGER,
    obr        INTEGER,   -- obrona
    trener_id  INTEGER REFERENCES trenerzy(id)
);

CREATE TABLE ataki (
    id    INTEGER PRIMARY KEY,
    nazwa TEXT    NOT NULL,
    typ   TEXT,
    moc   INTEGER,
    pp    INTEGER    -- ile razy można użyć
);

CREATE TABLE pokemon_ataki (
    pokemon_id INTEGER REFERENCES pokemony(id),
    atak_id    INTEGER REFERENCES ataki(id),
    PRIMARY KEY (pokemon_id, atak_id)
);

CREATE TABLE walki (
    id          INTEGER PRIMARY KEY,
    data        TEXT,
    zwyciezca_id INTEGER REFERENCES trenerzy(id),
    przegrany_id INTEGER REFERENCES trenerzy(id),
    arena       TEXT
);

-- ============================================================
--  DANE: TRENERZY
-- ============================================================

INSERT INTO trenerzy VALUES
(1,  'Ash',     10, 'Pallet Town',   8),
(2,  'Misty',   10, 'Cerulean City', 8),
(3,  'Brock',   15, 'Pewter City',   8),
(4,  'Gary',    10, 'Pallet Town',   9),
(5,  'Jessie',  18, 'Team Rocket',   1),
(6,  'James',   18, 'Team Rocket',   1),
(7,  'Serena',  12, 'Vaniville Town',5),
(8,  'Clemont', 13, 'Lumiose City',  6),
(9,  'Dawn',    10, 'Twinleaf Town', 7),
(10, 'May',     10, 'Petalburg City',5);

-- ============================================================
--  DANE: POKÉMONY
-- ============================================================

INSERT INTO pokemony VALUES
-- Ash
(1,  'Pikachu',    'Elektryczny', 35,  55, 40, 1),
(2,  'Charizard',  'Ogień',       78,  84, 78, 1),
(3,  'Bulbasaur',  'Trawa',       45,  49, 49, 1),
(4,  'Squirtle',   'Woda',        44,  48, 65, 1),
-- Misty
(5,  'Starmie',    'Woda',        60,  75, 85, 2),
(6,  'Psyduck',    'Woda',        50,  52, 48, 2),
(7,  'Goldeen',    'Woda',        45,  67, 60, 2),
-- Brock
(8,  'Onix',       'Skała',       35,  45,160, 3),
(9,  'Geodude',    'Skała',       40,  80,100, 3),
-- Gary
(10, 'Eevee',      'Normalny',    55,  55, 50, 4),
(11, 'Blastoise',  'Woda',        79,  83, 80, 4),
(12, 'Arcanine',   'Ogień',       90, 110, 80, 4),
-- Jessie
(13, 'Ekans',      'Trucizna',    35,  60, 44, 5),
(14, 'Wobbuffet',  'Psychiczny',  190, 33, 58, 5),
-- James
(15, 'Koffing',    'Trucizna',    40,  65, 95, 6),
(16, 'Growlithe',  'Ogień',       55,  70, 45, 6),
-- Serena
(17, 'Fennekin',   'Ogień',       40,  45, 40, 7),
(18, 'Pancham',    'Walka',       67,  82, 62, 7),
-- Clemont
(19, 'Dedenne',    'Elektryczny', 67,  58, 57, 8),
(20, 'Bunnelby',   'Normalny',    37,  36, 50, 8),
-- Dawn
(21, 'Piplup',     'Woda',        53,  51, 53, 9),
(22, 'Buneary',    'Normalny',    55,  66, 44, 9),
-- May
(23, 'Torchic',    'Ogień',       45,  60, 40, 10),
(24, 'Beautifly',  'Owad',        60,  70, 50, 10);

-- ============================================================
--  DANE: ATAKI
-- ============================================================

INSERT INTO ataki VALUES
(1,  'Thunderbolt',    'Elektryczny', 90,  15),
(2,  'Flamethrower',   'Ogień',       90,  15),
(3,  'Surf',           'Woda',        90,  15),
(4,  'Solarbeam',      'Trawa',      120,  10),
(5,  'Psychic',        'Psychiczny',  90,  10),
(6,  'Ice Beam',       'Lodowy',      90,  10),
(7,  'Earthquake',     'Ziemia',     100,  10),
(8,  'Tackle',         'Normalny',    40,  35),
(9,  'Quick Attack',   'Normalny',    40,  30),
(10, 'Ember',          'Ogień',       40,  25),
(11, 'Water Gun',      'Woda',        40,  25),
(12, 'Vine Whip',      'Trawa',       45,  25),
(13, 'Rock Throw',     'Skała',       50,  15),
(14, 'Poison Sting',   'Trucizna',    15,  35),
(15, 'Hyper Beam',     'Normalny',   150,   5);

-- ============================================================
--  DANE: KTÓRE POKÉMONY ZNAJĄ KTÓRE ATAKI
-- ============================================================

INSERT INTO pokemon_ataki VALUES
(1, 1), (1, 9), (1, 8),          -- Pikachu
(2, 2), (2, 15),(2, 7),          -- Charizard
(3, 12),(3, 4), (3, 8),          -- Bulbasaur
(4, 11),(4, 8), (4, 3),          -- Squirtle
(5, 3), (5, 5), (5, 6),          -- Starmie
(6, 11),(6, 8),                  -- Psyduck
(7, 11),(7, 8),                  -- Goldeen
(8, 13),(8, 7),                  -- Onix
(9, 13),(9, 8),                  -- Geodude
(10,8), (10,9),                  -- Eevee
(11,3), (11,15),(11,7),          -- Blastoise
(12,2), (12,15),(12,9),          -- Arcanine
(13,14),(13,8),                  -- Ekans
(14,8),                          -- Wobbuffet
(15,14),(15,8),                  -- Koffing
(16,2), (16,10),                 -- Growlithe
(17,10),(17,8),                  -- Fennekin
(18,8), (18,9),                  -- Pancham
(19,1), (19,8),                  -- Dedenne
(20,8),                          -- Bunnelby
(21,11),(21,3),                  -- Piplup
(22,8), (22,9),                  -- Buneary
(23,10),(23,8),                  -- Torchic
(24,8);                          -- Beautifly

-- ============================================================
--  DANE: WALKI
-- ============================================================

INSERT INTO walki VALUES
(1,  '2024-01-10', 1, 4,  'Cerulean Gym'),
(2,  '2024-01-15', 4, 1,  'Viridian Forest'),
(3,  '2024-01-20', 2, 5,  'Cerulean City'),
(4,  '2024-01-22', 3, 6,  'Pewter City'),
(5,  '2024-02-01', 1, 5,  'Viridian Forest'),
(6,  '2024-02-05', 1, 6,  'Viridian Forest'),
(7,  '2024-02-10', 4, 3,  'Victory Road'),
(8,  '2024-02-14', 7, 10, 'Lumiose City'),
(9,  '2024-02-18', 2, 10, 'Cerulean Gym'),
(10, '2024-03-01', 4, 2,  'Indigo Plateau'),
(11, '2024-03-05', 1, 7,  'Battle Tower'),
(12, '2024-03-10', 9, 8,  'Snowpoint City');