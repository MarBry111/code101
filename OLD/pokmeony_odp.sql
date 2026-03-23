================================================================
  POZIOM 1 — PIERWSZE KROKI
================================================================

-- Zadanie 1.
SELECT imie, wiek, miasto
FROM trenerzy;

-- Zadanie 2.
SELECT nazwa, hp, atak
FROM pokemony
WHERE typ = 'Ogień';

-- Zadanie 3.
SELECT nazwa, moc
FROM ataki
WHERE moc >= 90
ORDER BY moc DESC;

-- Zadanie 4.
SELECT nazwa, obr
FROM pokemony
WHERE obr > 80;

-- Zadanie 5.
SELECT imie, odznaki
FROM trenerzy
WHERE odznaki >= 8;

================================================================
  POZIOM 2 — SORTOWANIE I WARUNKI
================================================================

-- Zadanie 6.
SELECT nazwa, atak
FROM pokemony
ORDER BY atak DESC
LIMIT 5;

-- Zadanie 7.
SELECT nazwa, typ
FROM pokemony
WHERE trener_id = 5 OR trener_id = 6;

  -- Można też tak:
  SELECT nazwa, typ
  FROM pokemony
  WHERE trener_id IN (5, 6);

-- Zadanie 8.
SELECT nazwa, moc, pp
FROM ataki
WHERE pp <= 10
ORDER BY moc DESC;

-- Zadanie 9.
SELECT nazwa, typ, atak
FROM pokemony
WHERE typ = 'Elektryczny' OR typ = 'Trawa'
ORDER BY atak DESC;

================================================================
  POZIOM 3 — ŁĄCZENIE TABEL
================================================================

-- Zadanie 10.
SELECT t.imie, p.nazwa, p.typ
FROM trenerzy t
JOIN pokemony p ON p.trener_id = t.id
ORDER BY t.imie;

-- Zadanie 11.
SELECT t.imie, p.nazwa
FROM trenerzy t
JOIN pokemony p ON p.trener_id = t.id
WHERE p.typ = 'Woda';

-- Zadanie 12.
SELECT a.nazwa, a.moc
FROM pokemony p
JOIN pokemon_ataki pa ON pa.pokemon_id = p.id
JOIN ataki a          ON a.id = pa.atak_id
WHERE p.nazwa = 'Pikachu';

-- Zadanie 13.
SELECT w.data,
       zwyciezca.imie AS zwyciezca,
       przegrany.imie AS przegrany,
       w.arena
FROM walki w
JOIN trenerzy AS zwyciezca ON zwyciezca.id = w.zwyciezca_id
JOIN trenerzy AS przegrany ON przegrany.id = w.przegrany_id;

================================================================
  POZIOM 4 — MISJE DETEKTYWISTYCZNE
================================================================

-- Zadanie 14.
SELECT t.imie, p.nazwa, p.atak
FROM trenerzy t
JOIN pokemony p ON p.trener_id = t.id
WHERE p.atak > 80
  AND t.miasto = 'Pallet Town';

-- Zadanie 15. (część 1 — pokémony typu Skała)
SELECT t.imie, p.nazwa
FROM trenerzy t
JOIN pokemony p ON p.trener_id = t.id
WHERE p.typ = 'Skała';

-- Zadanie 15. (część 2 — czy Brock ma pokémona z Rock Throw)
SELECT p.nazwa, a.nazwa AS atak
FROM pokemony p
JOIN pokemon_ataki pa ON pa.pokemon_id = p.id
JOIN ataki a          ON a.id = pa.atak_id
JOIN trenerzy t       ON t.id = p.trener_id
WHERE t.imie = 'Brock'
  AND a.nazwa = 'Rock Throw';

-- Zadanie 16. — FINAŁOWE (można pisać krok po kroku)

-- Krok 1: jaki atak ma moc 150?
SELECT nazwa FROM ataki WHERE moc = 150;
-- Wynik: Hyper Beam

-- Krok 2 + 3 + 4: pełne zapytanie detektywistyczne
SELECT t.imie AS trener, p.nazwa AS pokemon, a.nazwa AS atak
FROM ataki a
JOIN pokemon_ataki pa ON pa.atak_id  = a.id
JOIN pokemony p       ON p.id        = pa.pokemon_id
JOIN trenerzy t       ON t.id        = p.trener_id
JOIN walki w          ON w.zwyciezca_id = t.id
WHERE a.moc = 150
  AND w.arena = 'Indigo Plateau';

-- Oczekiwany wynik:
--   trener  | pokemon   | atak
--   Gary    | Blastoise | Hyper Beam
--
--  Winowajca: Gary i jego Blastoise!

================================================================
  KONIEC ROZWIĄZAŃ
================================================================