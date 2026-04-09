from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
_db = None

def init_db():
    global _db
    _db = sqlite3.connect("file::memory:?cache=shared", uri=True, check_same_thread=False)
    cur = _db.cursor()
    cur.executescript("""
        -- Biblioteka
        CREATE TABLE czytelnicy (id INTEGER PRIMARY KEY, nick TEXT, email TEXT, rola TEXT);
        INSERT INTO czytelnicy VALUES (1,'bibliotekarz','bib@szkola.pl','admin');
        INSERT INTO czytelnicy VALUES (2,'tomek','tomek@mail.pl','user');
        INSERT INTO czytelnicy VALUES (3,'zosia','zosia@mail.pl','user');

        -- Gra
        CREATE TABLE gracze (id INTEGER PRIMARY KEY, nick TEXT, punkty INTEGER, sekret TEXT);
        INSERT INTO gracze VALUES (1,'ProGamer99',9999,'KOD_MISTRZA');
        INSERT INTO gracze VALUES (2,'tomek',350,'');
        INSERT INTO gracze VALUES (3,'zosia',210,'');

        -- Newsletter
        CREATE TABLE subskrybenci (id INTEGER PRIMARY KEY, email TEXT, aktywny INTEGER);
        INSERT INTO subskrybenci VALUES (1,'vip@firma.pl',1);
        INSERT INTO subskrybenci VALUES (2,'test@mail.pl',1);

        -- Bank (login + haslo)
        CREATE TABLE klienci_banku (id INTEGER PRIMARY KEY, login TEXT, pin TEXT, saldo REAL, rola TEXT);
        INSERT INTO klienci_banku VALUES (1,'dyrektor','0000',999999.99,'admin');
        INSERT INTO klienci_banku VALUES (2,'janek','1234',500.00,'user');

        -- Intranet firmy
        CREATE TABLE pracownicy (id INTEGER PRIMARY KEY, login TEXT, haslo TEXT, dzial TEXT, poziom TEXT);
        INSERT INTO pracownicy VALUES (1,'ceo','tajne!@#','Zarzad','admin');
        INSERT INTO pracownicy VALUES (2,'anna','qwerty','HR','user');

        -- Kino
        CREATE TABLE konta_kino (id INTEGER PRIMARY KEY, email TEXT, haslo TEXT, typ TEXT);
        INSERT INTO konta_kino VALUES (1,'admin@kino.pl','SuperHaslo!','admin');
        INSERT INTO konta_kino VALUES (2,'jan@mail.pl','haslo123','user');

        -- Ksiegarnia
        CREATE TABLE ksiazki (id INTEGER PRIMARY KEY, tytul TEXT, autor TEXT, ukryta INTEGER DEFAULT 0);
        INSERT INTO ksiazki VALUES (1,'Harry Potter','Rowling',0);
        INSERT INTO ksiazki VALUES (2,'Wiedźmin','Sapkowski',0);
        INSERT INTO ksiazki VALUES (3,'Pan Tadeusz','Mickiewicz',0);
        INSERT INTO ksiazki VALUES (4,'[TAJNE] Odpowiedzi do sprawdzianu','Nauczyciel',1);

        -- Filmy
        CREATE TABLE filmy (id INTEGER PRIMARY KEY, tytul TEXT, rok INTEGER, status TEXT);
        INSERT INTO filmy VALUES (1,'Avengers',2019,'publiczny');
        INSERT INTO filmy VALUES (2,'Spider-Man',2021,'publiczny');
        INSERT INTO filmy VALUES (3,'[PREMIERA] Nowy film 2025','2025','ukryty');

        -- Ogloszenia pracy
        CREATE TABLE oferty (id INTEGER PRIMARY KEY, stanowisko TEXT, firma TEXT, widoczna INTEGER DEFAULT 1);
        INSERT INTO oferty VALUES (1,'Programista Python','TechCorp',1);
        INSERT INTO oferty VALUES (2,'Grafik komputerowy','DesignHouse',1);
        INSERT INTO oferty VALUES (3,'[TAJNE] Szpieg korporacyjny','???',0);

        -- Przepisy (UNION target)
        CREATE TABLE tajne_przepisy (id INTEGER PRIMARY KEY, nazwa TEXT, skladniki TEXT);
        INSERT INTO tajne_przepisy VALUES (1,'Sekretna pizza','ser,sos,bazylia,TAJEMNICA');
        INSERT INTO tajne_przepisy VALUES (2,'Magiczny koktajl','mleko,miod,FLAG{PRZEPIS_ZNALEZIONY}');

        -- Forum (UNION target)
        CREATE TABLE prywatne_wiadomosci (id INTEGER PRIMARY KEY, od TEXT, tresc TEXT);
        INSERT INTO prywatne_wiadomosci VALUES (1,'admin','Hasło do serwera: FLAG{SERVER_PASS}');
        INSERT INTO prywatne_wiadomosci VALUES (2,'dyrektor','Spotkanie w piątek o 15:00');

        -- Kody rabatowe (UNION target)
        CREATE TABLE kody_rabatowe (id INTEGER PRIMARY KEY, kod TEXT, rabat TEXT);
        INSERT INTO kody_rabatowe VALUES (1,'FLAG{RABAT50}','50% zniżki na wszystko');
        INSERT INTO kody_rabatowe VALUES (2,'VIP2025','20% dla VIP');

        -- Klucze API (target kradziezy)
        CREATE TABLE api_keys (id INTEGER PRIMARY KEY, nazwa TEXT, klucz TEXT);
        INSERT INTO api_keys VALUES (1,'OpenAI','sk-TAJNY-KLUCZ-AI-12345');
        INSERT INTO api_keys VALUES (2,'Stripe','pk_live_KARTA_4567');

        -- Adresy email (target kradziezy)  
        CREATE TABLE zapisy (id INTEGER PRIMARY KEY, imie TEXT, email_prywatny TEXT);
        INSERT INTO zapisy VALUES (1,'Dyrektor','dyrektor.tajny@szkola.pl');
        INSERT INTO zapisy VALUES (2,'Sekretarka','sekretariat@szkola.pl');
    """)
    _db.commit()

def run_sql(sql):
    try:
        cur = _db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        return {"ok": True, "cols": cols, "rows": [list(r) for r in rows]}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/run", methods=["POST"])
def api_run():
    data = request.get_json()
    tpl = data.get("tpl", "")
    inp = data.get("input", "")
    sql = tpl.replace("__INPUT__", inp)
    if not sql.strip().upper().startswith("SELECT"):
        return jsonify({"ok": False, "error": "Tylko SELECT!", "sql": sql})
    r = run_sql(sql)
    r["sql"] = sql
    r["input"] = inp
    return jsonify(r)

# ===================== HTML =====================
HTML = r"""
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<title>SQL Injection — Zadania Samodzielne</title>
<link href="https://fonts.googleapis.com/css2?family=Syne:wght@400;700;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  --bg: #0c0c10;
  --surface: #13131a;
  --card: #18181f;
  --border: #252530;
  --border2: #2e2e3e;
  --text: #d4d4e0;
  --dim: #52526a;
  --accent: #7c6af7;
  --accent2: #4fd1c5;
  --warn: #f6ad55;
  --danger: #fc8181;
  --success: #68d391;
  --t1: #7c6af7;   /* technique 1 */
  --t2: #4fd1c5;   /* technique 2 */
  --t3: #f6ad55;   /* technique 3 */
  --t4: #fc8181;   /* technique 4 */
  --t5: #b794f4;   /* technique 5 */
}

body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Syne', sans-serif;
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* TOP */
.topbar {
  background: var(--surface);
  border-bottom: 1px solid var(--border);
  padding: 14px 28px;
  display: flex;
  align-items: center;
  gap: 14px;
  position: sticky; top: 0; z-index: 100;
}

.topbar h1 {
  font-size: 1rem;
  font-weight: 800;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--text);
}

.progress-bar {
  height: 3px;
  background: var(--border);
  border-radius: 2px;
  flex: 1;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--t1), var(--t5));
  border-radius: 2px;
  transition: width 0.4s ease;
  width: 0%;
}

.score-pill {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.78rem;
  color: var(--warn);
  background: rgba(246,173,85,0.1);
  border: 1px solid rgba(246,173,85,0.25);
  border-radius: 20px;
  padding: 5px 14px;
  white-space: nowrap;
}

/* MAIN */
.content {
  padding: 32px 28px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

.technique-block {
  margin-bottom: 48px;
}

.technique-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
  padding-bottom: 14px;
  border-bottom: 1px solid var(--border);
}

.technique-badge {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 600;
  letter-spacing: 1px;
  text-transform: uppercase;
  white-space: nowrap;
}

.t1 { background: rgba(124,106,247,0.15); color: var(--t1); border: 1px solid rgba(124,106,247,0.3); }
.t2 { background: rgba(79,209,197,0.12); color: var(--t2); border: 1px solid rgba(79,209,197,0.3); }
.t3 { background: rgba(246,173,85,0.12); color: var(--t3); border: 1px solid rgba(246,173,85,0.3); }
.t4 { background: rgba(252,129,129,0.12); color: var(--t4); border: 1px solid rgba(252,129,129,0.3); }
.t5 { background: rgba(183,148,244,0.12); color: var(--t5); border: 1px solid rgba(183,148,244,0.3); }

.technique-name {
  font-size: 1.1rem;
  font-weight: 800;
  color: var(--text);
}

.technique-desc {
  font-size: 0.83rem;
  color: var(--dim);
  margin-left: auto;
  font-family: 'JetBrains Mono', monospace;
}

/* TASK GRID */
.task-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
}

@media (max-width: 900px) { .task-grid { grid-template-columns: 1fr; } }

/* TASK CARD */
.task-card {
  background: var(--card);
  border: 1px solid var(--border);
  border-radius: 14px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  transition: border-color 0.2s;
}

.task-card:hover { border-color: var(--border2); }
.task-card.solved { border-color: rgba(104,211,145,0.4); }

.task-card-head {
  padding: 16px 18px 12px;
  border-bottom: 1px solid var(--border);
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.task-icon { font-size: 1.5rem; flex-shrink: 0; margin-top: 2px; }

.task-meta { flex: 1; }
.task-num {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.68rem;
  color: var(--dim);
  text-transform: uppercase;
  letter-spacing: 1px;
}
.task-title {
  font-size: 0.92rem;
  font-weight: 700;
  color: var(--text);
  margin-top: 2px;
  line-height: 1.3;
}

.task-solved-badge {
  font-size: 0.7rem;
  background: rgba(104,211,145,0.15);
  color: var(--success);
  border: 1px solid rgba(104,211,145,0.3);
  border-radius: 10px;
  padding: 2px 8px;
  display: none;
  white-space: nowrap;
}
.task-card.solved .task-solved-badge { display: inline; }

.task-body { padding: 14px 18px; flex: 1; display: flex; flex-direction: column; gap: 10px; }

.task-goal {
  font-size: 0.82rem;
  color: var(--dim);
  line-height: 1.6;
  flex: 1;
}

/* App UI inside card */
.mini-app {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 10px;
  overflow: hidden;
}

.mini-app-bar {
  background: #1e1e28;
  border-bottom: 1px solid var(--border);
  padding: 7px 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--dim);
  display: flex;
  align-items: center;
  gap: 6px;
}
.mini-dots { display:flex; gap:4px; }
.mini-dots span { width:7px; height:7px; border-radius:50%; }
.dot-r{background:#ff5f57;} .dot-y{background:#febc2e;} .dot-g{background:#28c840;}

.mini-body { padding: 12px; }

.field-label {
  font-size: 0.7rem;
  color: var(--dim);
  margin-bottom: 4px;
  font-family: 'JetBrains Mono', monospace;
}

.mini-input {
  width: 100%;
  background: #0c0c10;
  border: 1px solid var(--border2);
  border-radius: 6px;
  color: var(--text);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.82rem;
  padding: 8px 10px;
  outline: none;
  transition: border-color 0.2s;
}
.mini-input:focus { border-color: var(--accent); }

.mini-btn {
  margin-top: 8px;
  width: 100%;
  background: var(--accent);
  border: none;
  border-radius: 6px;
  color: white;
  font-family: 'Syne', sans-serif;
  font-weight: 700;
  font-size: 0.8rem;
  padding: 8px;
  cursor: pointer;
  transition: opacity 0.15s;
}
.mini-btn:hover { opacity: 0.85; }

/* color variants */
.mini-btn.c2 { background: var(--t2); color: #0c2a28; }
.mini-btn.c3 { background: var(--t3); color: #2a1800; }
.mini-btn.c4 { background: var(--t4); color: #2a0a0a; }
.mini-btn.c5 { background: var(--t5); color: #150a2a; }

/* result area */
.mini-result { margin-top: 8px; }

.result-ok {
  background: rgba(104,211,145,0.08);
  border: 1px solid rgba(104,211,145,0.2);
  border-radius: 6px;
  padding: 8px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--success);
  display: none;
  max-height: 130px;
  overflow-y: auto;
}
.result-ok table { width: 100%; border-collapse: collapse; }
.result-ok th { color: var(--t2); padding: 3px 6px; text-align: left; font-size: 0.65rem; border-bottom: 1px solid var(--border); }
.result-ok td { padding: 3px 6px; color: var(--text); font-size: 0.7rem; border-bottom: 1px solid rgba(255,255,255,0.03); }

.result-err {
  background: rgba(252,129,129,0.08);
  border: 1px solid rgba(252,129,129,0.2);
  border-radius: 6px;
  padding: 8px 10px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: var(--danger);
  display: none;
}

.result-empty {
  color: var(--dim);
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  text-align: center;
  padding: 8px;
  display: none;
}

.sql-trace {
  margin-top: 6px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.65rem;
  color: var(--border2);
  word-break: break-all;
  line-height: 1.5;
  display: none;
}

.success-pop {
  display: none;
  background: rgba(104,211,145,0.1);
  border: 1px solid rgba(104,211,145,0.3);
  border-radius: 8px;
  padding: 10px 12px;
  text-align: center;
  margin-top: 8px;
}
.success-pop h4 { color: var(--success); font-size: 0.85rem; }
.success-pop p { font-size: 0.75rem; color: var(--dim); margin-top: 4px; line-height: 1.4; }
</style>
</head>
<body>

<div class="topbar">
  <h1>🧪 SQL Injection — Zadania Samodzielne</h1>
  <div class="progress-bar"><div class="progress-fill" id="progressFill"></div></div>
  <div class="score-pill" id="scoreDisplay">⭐ 0 / 15 zaliczonych</div>
</div>

<div class="content">

<!-- ══════════ TECHNIKA 1 ══════════ -->
<div class="technique-block">
  <div class="technique-header">
    <span class="technique-badge t1">Technika 1</span>
    <div class="technique-name">OR '1'='1' — Jedno pole, zawsze prawda</div>
    <div class="technique-desc">WHERE field = '[INPUT]'</div>
  </div>
  <div class="task-grid">

    <!-- 1A -->
    <div class="task-card" id="card-1a">
      <div class="task-card-head">
        <div class="task-icon">📚</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 1A</div>
          <div class="task-title">Biblioteka szkolna</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Wyszukiwarka czytelników sprawdza tylko nick. Znajdź sposób, żeby wyświetlić <strong>wszystkich</strong> czytelników naraz — łącznie z bibliotekarze.</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>biblioteka.szkola.pl/szukaj</div>
          <div class="mini-body">
            <div class="field-label">Nick czytelnika:</div>
            <input class="mini-input" id="i1a" placeholder="wpisz nick...">
            <button class="mini-btn" onclick="run('1a', &quot;SELECT * FROM czytelnicy WHERE nick = '__INPUT__'&quot;, 'i1a', r => r.rows.length > 1)">🔍 Szukaj</button>
            <div class="mini-result" id="r1a"></div>
            <div class="success-pop" id="s1a"><h4>🎉 Brawo!</h4><p>Wyświetliłeś/aś wszystkich czytelników jednym zapytaniem!</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 1B -->
    <div class="task-card" id="card-1b">
      <div class="task-card-head">
        <div class="task-icon">🎮</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 1B</div>
          <div class="task-title">Tablica wyników gry</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Gra wyświetla wynik gracza po jego nicku. Gracz <strong>ProGamer99</strong> ma ukryty sekretny kod w kolumnie <em>sekret</em>. Wyświetl jego profil!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>supergra.pl/profil</div>
          <div class="mini-body">
            <div class="field-label">Nick gracza:</div>
            <input class="mini-input" id="i1b" placeholder="nick gracza...">
            <button class="mini-btn" onclick="run('1b', &quot;SELECT * FROM gracze WHERE nick = '__INPUT__'&quot;, 'i1b', r => r.rows.some(row => row[3] && row[3].length > 0))">🎯 Sprawdź wynik</button>
            <div class="mini-result" id="r1b"></div>
            <div class="success-pop" id="s1b"><h4>🎉 Udało się!</h4><p>Znalazłeś/aś sekretny kod ProGamera99!</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 1C -->
    <div class="task-card" id="card-1c">
      <div class="task-card-head">
        <div class="task-icon">📧</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 1C</div>
          <div class="task-title">Formularz newslettera</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Formularz sprawdza czy adres email jest zapisany do newslettera. Wymuś odpowiedź <strong>TAK</strong> dla dowolnego emaila — nawet nieistniejącego!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>newsletter.pl/sprawdz</div>
          <div class="mini-body">
            <div class="field-label">Twój adres email:</div>
            <input class="mini-input" id="i1c" placeholder="email@domena.pl">
            <button class="mini-btn" onclick="run('1c', &quot;SELECT * FROM subskrybenci WHERE email = '__INPUT__'&quot;, 'i1c', r => r.rows.length > 0)">✉️ Sprawdź subskrypcję</button>
            <div class="mini-result" id="r1c"></div>
            <div class="success-pop" id="s1c"><h4>🎉 Działa!</h4><p>Formularz twierdzi, że jesteś zapisany/a — nawet jeśli nie podałeś/aś prawdziwego emaila!</p></div>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>

<!-- ══════════ TECHNIKA 2 ══════════ -->
<div class="technique-block">
  <div class="technique-header">
    <span class="technique-badge t2">Technika 2</span>
    <div class="technique-name">Komentarz -- (pomiń hasło)</div>
    <div class="technique-desc">WHERE login='x'-- AND pass='...'</div>
  </div>
  <div class="task-grid">

    <!-- 2A -->
    <div class="task-card" id="card-2a">
      <div class="task-card-head">
        <div class="task-icon">🏦</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 2A</div>
          <div class="task-title">Panel banku online</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Bank sprawdza login i PIN. Zaloguj się jako <strong>dyrektor</strong> bez znajomości PINu. Użyj komentarza SQL!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>bank-bezpieczny.pl/login</div>
          <div class="mini-body">
            <div class="field-label">Login:</div>
            <input class="mini-input" id="i2a_u" placeholder="login...">
            <div class="field-label" style="margin-top:6px">PIN:</div>
            <input class="mini-input" id="i2a_p" placeholder="PIN..." type="password">
            <button class="mini-btn c2" onclick="run2('2a', &quot;SELECT * FROM klienci_banku WHERE login = '__U__' AND pin = '__P__'&quot;, 'i2a_u', 'i2a_p', r => r.rows.some(row => row[4]==='admin'))">🔐 Zaloguj</button>
            <div class="mini-result" id="r2a"></div>
            <div class="success-pop" id="s2a"><h4>🎉 Dostęp uzyskany!</h4><p>Zalogowałeś/aś się jako dyrektor banku bez PINu!</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 2B -->
    <div class="task-card" id="card-2b">
      <div class="task-card-head">
        <div class="task-icon">🏢</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 2B</div>
          <div class="task-title">Intranet firmy</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Intranet firmy wymaga loginu i hasła. Zaloguj się jako <strong>ceo</strong> (szef firmy) i uzyskaj dostęp do działu Zarząd!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>intranet.korporacja.pl</div>
          <div class="mini-body">
            <div class="field-label">Login pracownika:</div>
            <input class="mini-input" id="i2b_u" placeholder="login...">
            <div class="field-label" style="margin-top:6px">Hasło:</div>
            <input class="mini-input" id="i2b_p" placeholder="hasło..." type="password">
            <button class="mini-btn c2" onclick="run2('2b', &quot;SELECT * FROM pracownicy WHERE login = '__U__' AND haslo = '__P__'&quot;, 'i2b_u', 'i2b_p', r => r.rows.some(row => row[3]==='Zarzad'))">🏢 Wejdź</button>
            <div class="mini-result" id="r2b"></div>
            <div class="success-pop" id="s2b"><h4>🎉 Witaj, CEO!</h4><p>Masz teraz dostęp do tajnych dokumentów zarządu!</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 2C -->
    <div class="task-card" id="card-2c">
      <div class="task-card-head">
        <div class="task-icon">🎬</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 2C</div>
          <div class="task-title">Portal kinowy VIP</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Kino ma panel admina chroniony emailem i hasłem. Zaloguj się jako <strong>admin@kino.pl</strong> bez hasła, żeby zobaczyć niepublikowane filmy!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>kinoweb.pl/admin</div>
          <div class="mini-body">
            <div class="field-label">Email:</div>
            <input class="mini-input" id="i2c_u" placeholder="email@kino.pl">
            <div class="field-label" style="margin-top:6px">Hasło:</div>
            <input class="mini-input" id="i2c_p" placeholder="••••••" type="password">
            <button class="mini-btn c2" onclick="run2('2c', &quot;SELECT * FROM konta_kino WHERE email = '__U__' AND haslo = '__P__'&quot;, 'i2c_u', 'i2c_p', r => r.rows.some(row => row[3]==='admin'))">🎬 Zaloguj</button>
            <div class="mini-result" id="r2c"></div>
            <div class="success-pop" id="s2c"><h4>🎉 Dostęp VIP!</h4><p>Zalogowałeś/aś się jako administrator kina!</p></div>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>

<!-- ══════════ TECHNIKA 3 ══════════ -->
<div class="technique-block">
  <div class="technique-header">
    <span class="technique-badge t3">Technika 3</span>
    <div class="technique-name">Ominięcie warunku hidden/status</div>
    <div class="technique-desc">WHERE hidden=0 AND name LIKE '__INPUT__'</div>
  </div>
  <div class="task-grid">

    <!-- 3A -->
    <div class="task-card" id="card-3a">
      <div class="task-card-head">
        <div class="task-icon">📖</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 3A</div>
          <div class="task-title">Ksiegarnia online</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Ksiegarnia ukrywa jedną tajną książkę (<em>ukryta=1</em>). Wyszukaj wszystkie książki tak, żeby tajna też się pojawiła!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>ksiegarnia.pl/katalog</div>
          <div class="mini-body">
            <div class="field-label">Szukaj po tytule:</div>
            <input class="mini-input" id="i3a" placeholder="tytuł książki...">
            <button class="mini-btn c3" onclick="run('3a', &quot;SELECT id, tytul, autor FROM ksiazki WHERE ukryta = 0 AND tytul LIKE '%__INPUT__%'&quot;, 'i3a', r => r.rows.some(row => row[1] && row[1].includes('TAJNE')))">📚 Szukaj</button>
            <div class="mini-result" id="r3a"></div>
            <div class="success-pop" id="s3a"><h4>🎉 Znalazłeś/aś!</h4><p>Tajemnicza książka ujawniona! Warunek ukryta=0 przestał działać.</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3B -->
    <div class="task-card" id="card-3b">
      <div class="task-card-head">
        <div class="task-icon">🎥</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 3B</div>
          <div class="task-title">Baza filmów</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Portal filmowy ukrywa niepublikowane filmy (status = 'ukryty'). Znajdź film, który jeszcze nie miał premiery!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>filmweb-kopia.pl/szukaj</div>
          <div class="mini-body">
            <div class="field-label">Tytuł filmu:</div>
            <input class="mini-input" id="i3b" placeholder="szukaj filmu...">
            <button class="mini-btn c3" onclick="run('3b', &quot;SELECT id, tytul, rok FROM filmy WHERE status = 'publiczny' AND tytul LIKE '%__INPUT__%'&quot;, 'i3b', r => r.rows.some(row => row[1] && row[1].includes('PREMIERA')))">🎬 Szukaj</button>
            <div class="mini-result" id="r3b"></div>
            <div class="success-pop" id="s3b"><h4>🎉 Premiera ujawniona!</h4><p>Znalazłeś/aś film, który nie miał jeszcze oficjalnej premiery!</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 3C -->
    <div class="task-card" id="card-3c">
      <div class="task-card-head">
        <div class="task-icon">💼</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 3C</div>
          <div class="task-title">Tablica ogłoszeń pracy</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Portal pracy ukrywa jedną ofertę (widoczna=0). Znajdź tę tajemniczą, niewidoczną ofertę pracy!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>pracapl.pl/oferty</div>
          <div class="mini-body">
            <div class="field-label">Szukaj stanowiska:</div>
            <input class="mini-input" id="i3c" placeholder="np. programista...">
            <button class="mini-btn c3" onclick="run('3c', &quot;SELECT id, stanowisko, firma FROM oferty WHERE widoczna = 1 AND stanowisko LIKE '%__INPUT__%'&quot;, 'i3c', r => r.rows.some(row => row[1] && row[1].includes('TAJNE')))">💼 Szukaj ofert</button>
            <div class="mini-result" id="r3c"></div>
            <div class="success-pop" id="s3c"><h4>🎉 Oferta ujawniona!</h4><p>Znalazłeś/aś ukrytą ofertę pracy, której nie powinno być widać!</p></div>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>

<!-- ══════════ TECHNIKA 4 ══════════ -->
<div class="technique-block">
  <div class="technique-header">
    <span class="technique-badge t4">Technika 4</span>
    <div class="technique-name">UNION SELECT — dołącz inną tabelę</div>
    <div class="technique-desc">... UNION SELECT col1,col2,col3 FROM inna_tabela--</div>
  </div>
  <div class="task-grid">

    <!-- 4A -->
    <div class="task-card" id="card-4a">
      <div class="task-card-head">
        <div class="task-icon">🍕</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 4A</div>
          <div class="task-title">Portal z przepisami</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Wyszukiwarka przepisów zwraca <strong>3 kolumny</strong>: id, tytul, autor. Dołącz tabelę <code>tajne_przepisy</code> (też 3 kolumny: id, nazwa, skladniki)!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>przepisy.pl/szukaj</div>
          <div class="mini-body">
            <div class="field-label">Szukaj przepisu:</div>
            <input class="mini-input" id="i4a" placeholder="np. pizza lub użyj UNION...">
            <button class="mini-btn c4" onclick="run('4a', &quot;SELECT id, tytul, autor FROM ksiazki WHERE ukryta=0 AND tytul LIKE '%__INPUT__%'&quot;, 'i4a', r => r.rows.some(row => row.some(c => typeof c==='string' && c.includes('FLAG'))))">🔍 Szukaj</button>
            <div class="mini-result" id="r4a"></div>
            <div class="success-pop" id="s4a"><h4>🎉 Tajne przepisy wykradzione!</h4><p>UNION połączyło dwie tabele w jednym zapytaniu!</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 4B -->
    <div class="task-card" id="card-4b">
      <div class="task-card-head">
        <div class="task-icon">💬</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 4B</div>
          <div class="task-title">Forum — prywatne wiadomości</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Wyszukiwarka forum zwraca <strong>3 kolumny</strong>: id, stanowisko, firma. Dołącz tabelę <code>prywatne_wiadomosci</code> (id, od, tresc)!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>forum-szkolne.pl/szukaj</div>
          <div class="mini-body">
            <div class="field-label">Szukaj w forum:</div>
            <input class="mini-input" id="i4b" placeholder="temat lub atak UNION...">
            <button class="mini-btn c4" onclick="run('4b', &quot;SELECT id, stanowisko, firma FROM oferty WHERE widoczna=1 AND stanowisko LIKE '%__INPUT__%'&quot;, 'i4b', r => r.rows.some(row => row.some(c => typeof c==='string' && c.includes('FLAG'))))">🔍 Szukaj</button>
            <div class="mini-result" id="r4b"></div>
            <div class="success-pop" id="s4b"><h4>🎉 Prywatne wiadomości ujawnione!</h4><p>Odczytałeś/aś wiadomości, do których nie powinieneś/aś mieć dostępu!</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 4C -->
    <div class="task-card" id="card-4c">
      <div class="task-card-head">
        <div class="task-icon">🏷️</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 4C</div>
          <div class="task-title">Sklep — kody rabatowe</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Sklep wyszukuje filmy po tytule (3 kolumny: id, tytul, rok). Dołącz tabelę <code>kody_rabatowe</code> (id, kod, rabat) żeby zdobyć darmowe kody!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>supershop.pl/szukaj</div>
          <div class="mini-body">
            <div class="field-label">Szukaj produktu:</div>
            <input class="mini-input" id="i4c" placeholder="produkt lub atak UNION...">
            <button class="mini-btn c4" onclick="run('4c', &quot;SELECT id, tytul, rok FROM filmy WHERE status='publiczny' AND tytul LIKE '%__INPUT__%'&quot;, 'i4c', r => r.rows.some(row => row.some(c => typeof c==='string' && c.includes('FLAG'))))">🔍 Szukaj</button>
            <div class="mini-result" id="r4c"></div>
            <div class="success-pop" id="s4c"><h4>🎉 Kody zdobyte!</h4><p>Znalazłeś/aś tajne kody rabatowe ukryte w bazie!</p></div>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>

<!-- ══════════ TECHNIKA 5 ══════════ -->
<div class="technique-block">
  <div class="technique-header">
    <span class="technique-badge t5">Technika 5</span>
    <div class="technique-name">Kradzież danych z innej tabeli (UNION)</div>
    <div class="technique-desc">zaawansowany UNION na tabele z wrażliwymi danymi</div>
  </div>
  <div class="task-grid">

    <!-- 5A -->
    <div class="task-card" id="card-5a">
      <div class="task-card-head">
        <div class="task-icon">🔑</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 5A</div>
          <div class="task-title">Wykradnij klucze API</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Wyszukiwarka czytelników (3 kolumny: id, nick, email). W bazie jest tabela <code>api_keys</code> (id, nazwa, klucz). Wykradnij klucze API przez UNION!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>biblioteka.szkola.pl/szukaj</div>
          <div class="mini-body">
            <div class="field-label">Szukaj czytelnika:</div>
            <input class="mini-input" id="i5a" placeholder="nick lub atak UNION...">
            <button class="mini-btn c5" onclick="run('5a', &quot;SELECT id, nick, email FROM czytelnicy WHERE nick LIKE '%__INPUT__%'&quot;, 'i5a', r => r.rows.some(row => row.some(c => typeof c==='string' && c.includes('sk-'))))">🔍 Szukaj</button>
            <div class="mini-result" id="r5a"></div>
            <div class="success-pop" id="s5a"><h4>🎉 Klucze API wykradzione!</h4><p>Znalazłeś/aś tajne klucze API ukryte w zupełnie innej tabeli!</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 5B -->
    <div class="task-card" id="card-5b">
      <div class="task-card-head">
        <div class="task-icon">📨</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 5B</div>
          <div class="task-title">Wykradnij prywatne emaile</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Wyszukiwarka gracza (3 kolumny: id, nick, punkty). W bazie jest tabela <code>zapisy</code> (id, imie, email_prywatny). Wyciągnij prywatne adresy email!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>supergra.pl/ranking</div>
          <div class="mini-body">
            <div class="field-label">Szukaj gracza:</div>
            <input class="mini-input" id="i5b" placeholder="nick gracza...">
            <button class="mini-btn c5" onclick="run('5b', &quot;SELECT id, nick, punkty FROM gracze WHERE nick LIKE '%__INPUT__%'&quot;, 'i5b', r => r.rows.some(row => row.some(c => typeof c==='string' && c.includes('@szkola'))))">🔍 Szukaj</button>
            <div class="mini-result" id="r5b"></div>
            <div class="success-pop" id="s5b"><h4>🎉 Emaile wykradzione!</h4><p>Uzyskałeś/aś dostęp do prywatnych adresów email ze szkoły!</p></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 5C -->
    <div class="task-card" id="card-5c">
      <div class="task-card-head">
        <div class="task-icon">👑</div>
        <div class="task-meta">
          <div class="task-num">Zadanie 5C</div>
          <div class="task-title">Hasła pracowników firmy</div>
        </div>
        <div class="task-solved-badge">✓ Zaliczone</div>
      </div>
      <div class="task-body">
        <div class="task-goal">Wyszukiwarka filmów (3 kolumny: id, tytul, rok). Wykradnij hasła z tabeli <code>pracownicy</code> (id, login, haslo) — tylko dla działu Zarząd!</div>
        <div class="mini-app">
          <div class="mini-app-bar"><div class="mini-dots"><span class="dot-r"></span><span class="dot-y"></span><span class="dot-g"></span></div>kinoweb.pl/filmy</div>
          <div class="mini-body">
            <div class="field-label">Szukaj filmu:</div>
            <input class="mini-input" id="i5c" placeholder="tytuł lub atak UNION...">
            <button class="mini-btn c5" onclick="run('5c', &quot;SELECT id, tytul, rok FROM filmy WHERE status='publiczny' AND tytul LIKE '%__INPUT__%'&quot;, 'i5c', r => r.rows.some(row => row.some(c => typeof c==='string' && c.includes('tajne'))))">🔍 Szukaj</button>
            <div class="mini-result" id="r5c"></div>
            <div class="success-pop" id="s5c"><h4>🏆 MISTRZ SQL INJECTION!</h4><p>Wykradłeś/aś hasło CEO firmy przez wyszukiwarkę filmów!</p></div>
          </div>
        </div>
      </div>
    </div>

  </div>
</div>

</div><!-- /content -->

<script>
let solved = new Set();

async function run(id, tpl, inputId, checkFn) {
  const inp = document.getElementById(inputId).value;
  const res = await fetch('/api/run', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({tpl, input: inp})
  });
  const data = await res.json();
  renderResult(id, data);
  if (data.ok && checkFn(data)) markSolved(id);
}

async function run2(id, tpl, userInputId, passInputId, checkFn) {
  const u = document.getElementById(userInputId).value;
  const p = document.getElementById(passInputId).value;
  const filled = tpl.replace('__U__', u).replace('__P__', p);
  const res = await fetch('/api/run', {
    method: 'POST',
    headers: {'Content-Type':'application/json'},
    body: JSON.stringify({tpl: filled, input: ''})
  });
  const data = await res.json();
  data.sql = filled; // already built
  renderResult(id, data);
  if (data.ok && checkFn(data)) markSolved(id);
}

function renderResult(id, data) {
  const area = document.getElementById('r' + id);
  if (!data.ok) {
    area.innerHTML = `<div class="result-err" style="display:block">⚠️ ${data.error}</div>`;
    return;
  }
  if (!data.rows || data.rows.length === 0) {
    area.innerHTML = `<div class="result-empty" style="display:block">Brak wyników (0 wierszy)</div>`;
    return;
  }
  let tbl = '<div class="result-ok" style="display:block"><table><thead><tr>';
  (data.cols || []).forEach(c => tbl += `<th>${c}</th>`);
  tbl += '</tr></thead><tbody>';
  data.rows.forEach(row => {
    tbl += '<tr>';
    row.forEach(cell => tbl += `<td>${cell ?? ''}</td>`);
    tbl += '</tr>';
  });
  tbl += `</tbody></table></div>`;
  area.innerHTML = tbl;
}

function markSolved(id) {
  if (solved.has(id)) return;
  solved.add(id);
  document.getElementById('card-' + id).classList.add('solved');
  const sp = document.getElementById('s' + id);
  if (sp) sp.style.display = 'block';
  document.getElementById('scoreDisplay').textContent = `⭐ ${solved.size} / 15 zaliczonych`;
  document.getElementById('progressFill').style.width = (solved.size / 15 * 100) + '%';
}
</script>
</body>
</html>
"""

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  🧪  SQL INJECTION — Zadania Samodzielne")
    print("="*55)
    print("  Otwórz przeglądarkę i wejdź na:")
    print("  ➜  http://localhost:5002")
    print("="*55 + "\n")
    init_db()
    app.run(debug=False, port=5002)