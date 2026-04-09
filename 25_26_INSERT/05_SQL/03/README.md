# 🔐 SQL Injection Quest — Aplikacja Edukacyjna

Interaktywna gra do nauki ataków SQL Injection dla dzieci ok. 13 lat.
Wszystko działa lokalnie, bezpiecznie, na bazie in-memory SQLite.

---

## ▶ Uruchomienie (VSCode / terminal)

### 1. Zainstaluj zależności
```bash
pip install flask
```

### 2. Uruchom aplikację
```bash
python app2.py
```

### 3. Otwórz przeglądarkę
```
http://localhost:5001
```

---

## 🎮 Poziomy (5 zadań)

| # | Nazwa | Technika |
|---|-------|----------|
| 1 | Wyłam drzwi logowania | `OR '1'='1'` — zawsze prawda |
| 2 | Pomiń hasło komentarzem | `--` komentarz w SQL |
| 3 | Znajdź ukryty skarb | Bypass warunku `hidden = 0` |
| 4 | Odczytaj ukrytą tabelę | `UNION SELECT` |
| 5 | Zdobądź hasło admina | `UNION SELECT` + filtrowanie |

---

## 🛡️ Bezpieczeństwo

- Baza danych jest **wyłącznie w pamięci RAM** (SQLite in-memory)
- Dozwolone są tylko zapytania `SELECT`
- Dane są fikcyjne i zresetują się po restarcie
- Aplikacja działa **tylko lokalnie** (localhost)

---

## 📚 Co uczniowie się nauczą?

1. Jak działają zapytania SQL
2. Dlaczego niezabezpieczone inputy są niebezpieczne
3. Klasyczne techniki SQL Injection
4. Jak UNION pozwala łączyć dane z różnych tabel
5. Dlaczego programiści powinni używać **prepared statements**
