from flask import Flask, request, jsonify, render_template_string
import sqlite3
import os

app = Flask(__name__)
DB_PATH = ":memory:"

# --- DATABASE SETUP ---
def get_db():
    conn = sqlite3.connect(":memory:")
    return conn

# Global in-memory database (persistent for app lifetime)
_db = None

def init_db():
    global _db
    _db = sqlite3.connect("file::memory:?cache=shared", uri=True, check_same_thread=False)
    cur = _db.cursor()

    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            password TEXT,
            role TEXT
        );

        INSERT INTO users VALUES (1, 'admin', 'SuperTajneHaslo123', 'admin');
        INSERT INTO users VALUES (2, 'janek', 'kot123', 'user');
        INSERT INTO users VALUES (3, 'ania', 'piesek456', 'user');
        INSERT INTO users VALUES (4, 'bartek', 'dragon789', 'user');

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY,
            name TEXT,
            price REAL,
            hidden INTEGER DEFAULT 0
        );

        INSERT INTO products VALUES (1, 'Kredki Faber-Castell', 19.99, 0);
        INSERT INTO products VALUES (2, 'Zeszyt A4', 3.50, 0);
        INSERT INTO products VALUES (3, 'Plecak szkolny', 89.00, 0);
        INSERT INTO products VALUES (4, '🏆 TAJNY SKARB - Złota Odznaka', 0.01, 1);

        CREATE TABLE IF NOT EXISTS secret_codes (
            id INTEGER PRIMARY KEY,
            code TEXT,
            description TEXT
        );

        INSERT INTO secret_codes VALUES (1, 'FLAG{SQL_W1Z4RD}', 'Kod mistrza SQL');
        INSERT INTO secret_codes VALUES (2, 'FLAG{H4CK3R_K1D}', 'Kod hakera dziecięcego');
    """)
    _db.commit()

def query_db(sql, params=None):
    try:
        cur = _db.cursor()
        if params:
            cur.execute(sql, params)
        else:
            cur.execute(sql)
        rows = cur.fetchall()
        col_names = [desc[0] for desc in cur.description] if cur.description else []
        return {"success": True, "columns": col_names, "rows": rows, "count": len(rows)}
    except Exception as e:
        return {"success": False, "error": str(e), "columns": [], "rows": []}

# ==================== HTML TEMPLATE ====================
HTML = r"""
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<title>🔐 SQL Injection Quest</title>
<link href="https://fonts.googleapis.com/css2?family=Share+Tech+Mono&family=Exo+2:wght@400;700;900&display=swap" rel="stylesheet">
<style>
  :root {
    --bg: #0a0e1a;
    --panel: #0f1729;
    --border: #1e3a5f;
    --green: #00ff88;
    --cyan: #00d4ff;
    --yellow: #ffd700;
    --red: #ff4466;
    --text: #c8d8e8;
    --dim: #4a6080;
  }

  * { box-sizing: border-box; margin: 0; padding: 0; }

  body {
    background: var(--bg);
    font-family: 'Exo 2', sans-serif;
    color: var(--text);
    min-height: 100vh;
    background-image:
      radial-gradient(ellipse at 20% 50%, rgba(0,80,160,0.08) 0%, transparent 60%),
      radial-gradient(ellipse at 80% 20%, rgba(0,200,100,0.05) 0%, transparent 50%);
  }

  header {
    padding: 24px 40px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 16px;
    background: rgba(15,23,41,0.8);
    backdrop-filter: blur(10px);
    position: sticky; top: 0; z-index: 100;
  }

  header h1 {
    font-family: 'Share Tech Mono', monospace;
    font-size: 1.4rem;
    color: var(--green);
    text-shadow: 0 0 20px rgba(0,255,136,0.4);
    letter-spacing: 2px;
  }

  .score-badge {
    margin-left: auto;
    background: rgba(255,215,0,0.1);
    border: 1px solid var(--yellow);
    border-radius: 20px;
    padding: 6px 18px;
    font-family: 'Share Tech Mono', monospace;
    color: var(--yellow);
    font-size: 0.9rem;
  }

  .container {
    max-width: 1100px;
    margin: 0 auto;
    padding: 30px 20px;
    display: grid;
    grid-template-columns: 260px 1fr;
    gap: 24px;
  }

  /* SIDEBAR */
  .sidebar { display: flex; flex-direction: column; gap: 12px; }

  .level-btn {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 14px 16px;
    cursor: pointer;
    text-align: left;
    transition: all 0.2s;
    color: var(--text);
    font-family: 'Exo 2', sans-serif;
  }

  .level-btn:hover { border-color: var(--cyan); color: var(--cyan); }
  .level-btn.active { border-color: var(--green); background: rgba(0,255,136,0.07); }
  .level-btn.solved { border-color: var(--green); }
  .level-btn .lnum { font-size: 0.7rem; color: var(--dim); font-family: 'Share Tech Mono', monospace; }
  .level-btn .ltitle { font-weight: 700; font-size: 0.95rem; margin-top: 2px; }
  .level-btn .lcheck { float: right; color: var(--green); font-size: 1.2rem; }

  /* MAIN PANEL */
  .main-panel { display: flex; flex-direction: column; gap: 20px; }

  .card {
    background: var(--panel);
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
  }

  .card-header {
    padding: 16px 22px;
    border-bottom: 1px solid var(--border);
    display: flex;
    align-items: center;
    gap: 10px;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    color: var(--dim);
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .card-header .dot { width: 8px; height: 8px; border-radius: 50%; }
  .dot-green { background: var(--green); box-shadow: 0 0 6px var(--green); }
  .dot-cyan  { background: var(--cyan);  box-shadow: 0 0 6px var(--cyan); }
  .dot-yellow{ background: var(--yellow);box-shadow: 0 0 6px var(--yellow); }

  .card-body { padding: 20px 22px; }

  .mission-title {
    font-size: 1.4rem;
    font-weight: 900;
    color: var(--cyan);
    margin-bottom: 8px;
  }

  .mission-desc {
    line-height: 1.7;
    color: var(--text);
    font-size: 0.95rem;
  }

  /* SQL Query input area */
  .sql-area {
    position: relative;
  }

  .sql-label {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: var(--dim);
    margin-bottom: 6px;
    text-transform: uppercase;
    letter-spacing: 1px;
  }

  .sql-prefix {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    color: var(--dim);
    background: rgba(0,0,0,0.3);
    border: 1px solid var(--border);
    border-right: none;
    border-radius: 8px 0 0 8px;
    padding: 12px 14px;
    white-space: pre;
    line-height: 1.5;
    display: inline-block;
    vertical-align: top;
  }

  .input-row { display: flex; align-items: stretch; }

  textarea.sql-input {
    flex: 1;
    background: rgba(0,212,255,0.04);
    border: 1px solid var(--cyan);
    border-radius: 0 8px 8px 0;
    color: var(--cyan);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.95rem;
    padding: 12px 14px;
    resize: vertical;
    min-height: 52px;
    outline: none;
    transition: border-color 0.2s, box-shadow 0.2s;
    line-height: 1.5;
  }

  textarea.sql-input:focus {
    border-color: var(--green);
    box-shadow: 0 0 0 3px rgba(0,255,136,0.1);
  }

  .run-btn {
    background: linear-gradient(135deg, var(--green), #00cc66);
    border: none;
    border-radius: 8px;
    color: #0a0e1a;
    font-family: 'Exo 2', sans-serif;
    font-weight: 900;
    font-size: 1rem;
    padding: 12px 28px;
    cursor: pointer;
    margin-top: 12px;
    transition: all 0.2s;
    letter-spacing: 1px;
  }

  .run-btn:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(0,255,136,0.3); }
  .run-btn:active { transform: translateY(0); }

  /* Results */
  .result-area { margin-top: 16px; }

  table.result-table {
    width: 100%;
    border-collapse: collapse;
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.82rem;
  }

  table.result-table th {
    background: rgba(0,212,255,0.1);
    color: var(--cyan);
    padding: 8px 12px;
    text-align: left;
    border-bottom: 1px solid var(--border);
    text-transform: uppercase;
    letter-spacing: 1px;
    font-size: 0.7rem;
  }

  table.result-table td {
    padding: 8px 12px;
    border-bottom: 1px solid rgba(30,58,95,0.5);
    color: var(--text);
  }

  table.result-table tr:last-child td { border-bottom: none; }
  table.result-table tr:hover td { background: rgba(255,255,255,0.02); }

  .result-error {
    color: var(--red);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    padding: 10px;
    background: rgba(255,68,102,0.08);
    border: 1px solid rgba(255,68,102,0.2);
    border-radius: 6px;
  }

  .result-empty {
    color: var(--dim);
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.85rem;
    text-align: center;
    padding: 20px;
  }

  /* Success banner */
  .success-banner {
    display: none;
    background: linear-gradient(135deg, rgba(0,255,136,0.12), rgba(0,212,255,0.08));
    border: 1px solid var(--green);
    border-radius: 10px;
    padding: 18px 22px;
    text-align: center;
    animation: pulse-glow 2s ease-in-out infinite;
  }

  .success-banner.show { display: block; }

  @keyframes pulse-glow {
    0%, 100% { box-shadow: 0 0 10px rgba(0,255,136,0.2); }
    50% { box-shadow: 0 0 25px rgba(0,255,136,0.4); }
  }

  .success-banner h3 { color: var(--green); font-size: 1.3rem; margin-bottom: 6px; }
  .success-banner p { color: var(--text); font-size: 0.9rem; }

  /* Schema viewer */
  .schema-block {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.8rem;
    line-height: 1.8;
    color: var(--dim);
  }
  .schema-block .kw { color: var(--cyan); }
  .schema-block .tbl { color: var(--yellow); }
  .schema-block .col { color: var(--green); }

  .rows-count {
    font-family: 'Share Tech Mono', monospace;
    font-size: 0.75rem;
    color: var(--dim);
    margin-top: 8px;
    text-align: right;
  }

  @media (max-width: 700px) {
    .container { grid-template-columns: 1fr; }
    .sidebar { flex-direction: row; flex-wrap: wrap; }
    .level-btn { flex: 1; min-width: 140px; }
  }
</style>
</head>
<body>

<header>
  <div style="font-size:1.6rem">🔐</div>
  <h1>SQL INJECTION QUEST</h1>
  <div class="score-badge" id="scoreDisplay">⭐ 0 / 5 zadań</div>
</header>

<div class="container">
  <!-- SIDEBAR -->
  <aside class="sidebar">
    <div class="level-btn active" onclick="loadLevel(0)" id="lb0">
      <div class="lnum">POZIOM 1</div>
      <div class="ltitle">🔑 Wyłam drzwi</div>
      <span class="lcheck" id="lc0" style="display:none">✓</span>
    </div>
    <div class="level-btn" onclick="loadLevel(1)" id="lb1">
      <div class="lnum">POZIOM 2</div>
      <div class="ltitle">🗑️ Pomiń hasło</div>
      <span class="lcheck" id="lc1" style="display:none">✓</span>
    </div>
    <div class="level-btn" onclick="loadLevel(2)" id="lb2">
      <div class="lnum">POZIOM 3</div>
      <div class="ltitle">👁️ Znajdź skarb</div>
      <span class="lcheck" id="lc2" style="display:none">✓</span>
    </div>
    <div class="level-btn" onclick="loadLevel(3)" id="lb3">
      <div class="lnum">POZIOM 4</div>
      <div class="ltitle">🗂️ Ukryta tabela</div>
      <span class="lcheck" id="lc3" style="display:none">✓</span>
    </div>
    <div class="level-btn" onclick="loadLevel(4)" id="lb4">
      <div class="lnum">POZIOM 5</div>
      <div class="ltitle">👑 Hasło admina</div>
      <span class="lcheck" id="lc4" style="display:none">✓</span>
    </div>

    <!-- Schema card -->
    <div class="card" style="margin-top:12px">
      <div class="card-header"><div class="dot dot-yellow"></div>Struktura bazy</div>
      <div class="card-body">
        <div class="schema-block">
          <span class="kw">TABLE</span> <span class="tbl">users</span><br>
          &nbsp;<span class="col">id, username</span><br>
          &nbsp;<span class="col">password, role</span><br><br>
          <span class="kw">TABLE</span> <span class="tbl">products</span><br>
          &nbsp;<span class="col">id, name</span><br>
          &nbsp;<span class="col">price, hidden</span><br><br>
          <span class="kw">TABLE</span> <span class="tbl">secret_codes</span><br>
          &nbsp;<span class="col">id, code</span><br>
          &nbsp;<span class="col">description</span>
        </div>
      </div>
    </div>
  </aside>

  <!-- MAIN -->
  <main class="main-panel">
    <!-- Mission card -->
    <div class="card">
      <div class="card-header">
        <div class="dot dot-cyan"></div>
        <span id="missionLabel">MISJA 1</span>
      </div>
      <div class="card-body">
        <div class="mission-title" id="missionTitle">🔑 Wyłam drzwi logowania</div>
        <div class="mission-desc" id="missionDesc"></div>

      </div>
    </div>

    <!-- Query card -->
    <div class="card">
      <div class="card-header">
        <div class="dot dot-green"></div>
        TERMINAL SQL
      </div>
      <div class="card-body">
        <div class="sql-label">Wpisz swoją "broń" (SQL injection):</div>
        <div class="input-row">
          <div class="sql-prefix" id="sqlPrefix">SELECT * FROM users
WHERE username = '</div>
          <textarea class="sql-input" id="sqlInput" rows="2" placeholder="wpisz tutaj..." onkeydown="handleKey(event)"></textarea>
        </div>
        <button class="run-btn" onclick="runQuery()">▶ URUCHOM ATAK</button>

        <div class="result-area" id="resultArea"></div>
        <div class="success-banner" id="successBanner">
          <h3>🎉 POZIOM ZALICZONY!</h3>
          <p id="successMsg"></p>
        </div>
      </div>
    </div>
  </main>
</div>

<script>
const levels = [
  {
    id: 0,
    label: "MISJA 1",
    title: "🔑 Wyłam drzwi logowania",
    desc: `Aplikacja loguje użytkowników tym zapytaniem SQL:<br><br>
<code style="color:#00d4ff;font-family:monospace">SELECT * FROM users WHERE username = '[TWÓJ INPUT]'</code><br><br>
Twoim zadaniem jest <strong>zalogować się jako admin</strong> bez znajomości hasła!<br><br>
Baza ma użytkowników: <strong>admin</strong>, janek, ania, bartek.<br>
Spróbuj "złamać" formularz tak, aby zapytanie zwróciło użytkownika admin. 🕵️`,
    prefix: `SELECT * FROM users\nWHERE username = '`,
    suffix: `'`,
    level: 0,
    check: (rows) => rows.some(r => r[1] === 'admin' || r[3] === 'admin')
  },
  {
    id: 1,
    label: "MISJA 2",
    title: "🗑️ Pomiń hasło komentarzem",
    desc: `Tym razem aplikacja sprawdza ZARÓWNO login jak i hasło:<br><br>
<code style="color:#00d4ff;font-family:monospace">SELECT * FROM users WHERE username = '[INPUT]' AND password = 'cokolwiek'</code><br><br>
Musisz zalogować się jako <strong>admin</strong>, ale znasz tylko nazwę użytkownika.<br>
SQL ma specjalny symbol komentarza — użyj go, żeby <em>ukryć</em> część z hasłem! 😈`,
    prefix: `SELECT * FROM users\nWHERE username = '`,
    suffix: `' AND password = 'cokolwiek'`,
    level: 1,
    check: (rows) => rows.length > 0 && rows[0][1] === 'admin'
  },
  {
    id: 2,
    label: "MISJA 3",
    title: "👁️ Znajdź ukryty skarb",
    desc: `Sklep pokazuje produkty normalnym zapytaniem:<br><br>
<code style="color:#00d4ff;font-family:monospace">SELECT * FROM products WHERE hidden = 0 AND name LIKE '[INPUT]'</code><br><br>
Ale w bazie jest <strong>ukryty produkt</strong> (hidden = 1) — tajny skarb! 🏆<br>
Musisz tak zmanipulować zapytanie, żeby pokazało WSZYSTKIE produkty, łącznie z ukrytymi!`,
    prefix: `SELECT * FROM products\nWHERE hidden = 0\nAND name LIKE '`,
    suffix: `'`,
    level: 2,
    check: (rows) => rows.some(r => r[4] === 1 || (r[2] && r[2].toString().includes('SKARB')))
  },
  {
    id: 3,
    label: "MISJA 4",
    title: "🗂️ Odczytaj ukrytą tabelę",
    desc: `Zaawansowany atak! Używamy <strong>UNION</strong> — można nim "przykleić" wyniki z INNEJ tabeli.<br><br>
<code style="color:#00d4ff;font-family:monospace">SELECT id, name, price FROM products WHERE name LIKE '[INPUT]'</code><br><br>
W bazie jest tajemnicza tabela <code>secret_codes</code> z kodami.<br>
Użyj UNION SELECT żeby ją odczytać razem z produktami! 🧩<br><br>
<em>Uwaga: UNION wymaga tej samej liczby kolumn (tutaj 3)!</em>`,
    prefix: `SELECT id, name, price\nFROM products\nWHERE name LIKE '`,
    suffix: `'`,
    level: 3,
    check: (rows) => rows.some(r => r.some(c => typeof c === 'string' && c.includes('FLAG')))
  },
  {
    id: 4,
    label: "MISJA 5",
    title: "👑 Zdobądź hasło admina",
    desc: `Finałowe wyzwanie! Połącz wszystkie umiejętności.<br><br>
<code style="color:#00d4ff;font-family:monospace">SELECT id, name, price FROM products WHERE name LIKE '[INPUT]'</code><br><br>
Twoim celem jest wyciągnąć <strong>hasło admina</strong> z tabeli <code>users</code> używając ataku UNION.<br><br>
Pamiętaj: potrzebujesz 3 kolumn. Wybierz <code>id, username, password</code> z tabeli users,<br>
ale tylko dla użytkownika o roli 'admin'. 🎯`,
    prefix: `SELECT id, name, price\nFROM products\nWHERE name LIKE '`,
    suffix: `'`,
    level: 4,
    check: (rows) => rows.some(r => r.some(c => typeof c === 'string' && c.includes('SuperTajne')))
  }
];

let currentLevel = 0;
let solved = new Set();

function loadLevel(idx) {
  currentLevel = idx;
  const lv = levels[idx];
  document.getElementById('missionLabel').textContent = lv.label;
  document.getElementById('missionTitle').textContent = lv.title;
  document.getElementById('missionDesc').innerHTML = lv.desc;
  document.getElementById('sqlPrefix').textContent = lv.prefix;
  document.getElementById('sqlInput').value = '';
  document.getElementById('resultArea').innerHTML = '';
  document.getElementById('successBanner').classList.remove('show');

  document.querySelectorAll('.level-btn').forEach((b, i) => {
    b.classList.toggle('active', i === idx);
  });
}



function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    runQuery();
  }
}

async function runQuery() {
  const lv = levels[currentLevel];
  const userInput = document.getElementById('sqlInput').value;
  const fullSQL = `${lv.prefix}${userInput}${lv.suffix}`;

  const res = await fetch('/run', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({ sql: fullSQL, level: currentLevel })
  });
  const data = await res.json();

  renderResult(data);

  if (data.success && lv.check(data.rows)) {
    markSolved(currentLevel, userInput);
  }
}

function renderResult(data) {
  const area = document.getElementById('resultArea');
  if (!data.success) {
    area.innerHTML = `<div class="result-error">❌ Błąd SQL: ${data.error}</div>`;
    return;
  }
  if (data.rows.length === 0) {
    area.innerHTML = `<div class="result-empty">Zapytanie wykonane — brak wyników (0 wierszy)</div>`;
    return;
  }
  let html = `<table class="result-table"><thead><tr>`;
  data.columns.forEach(c => html += `<th>${c}</th>`);
  html += `</tr></thead><tbody>`;
  data.rows.forEach(row => {
    html += '<tr>';
    row.forEach(cell => html += `<td>${cell !== null ? cell : '<em style="color:var(--dim)">NULL</em>'}</td>`);
    html += '</tr>';
  });
  html += `</tbody></table>`;
  html += `<div class="rows-count">↳ ${data.rows.length} wiersz(y) zwrócono</div>`;
  area.innerHTML = html;
}

function markSolved(idx, input) {
  solved.add(idx);
  document.getElementById(`lc${idx}`).style.display = 'inline';
  document.getElementById(`lb${idx}`).classList.add('solved');
  document.getElementById('successBanner').classList.add('show');

  const msgs = [
    "Brawo! Ominąłeś/ominęłaś logowanie używając OR '1'='1'! To klasyczny SQL Injection!",
    "Niesamowite! Komentarz -- 'zabił' część zapytania z hasłem!",
    "Świetnie! Ukryty produkt ujawniony! Warunek hidden=0 nie miał już znaczenia!",
    "Ekstra! Użyłeś/użyłaś UNION żeby odczytać całkowicie inną tabelę!",
    "🏆 MISTRZ SQL INJECTION! Wyciągnąłeś/wyciągnęłaś hasło admina bez dostępu!"
  ];
  document.getElementById('successMsg').textContent = msgs[idx] || "Poziom zaliczony!";
  document.getElementById('scoreDisplay').textContent = `⭐ ${solved.size} / 5 zadań`;
}

// Init
loadLevel(0);
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/run", methods=["POST"])
def run():
    data = request.get_json()
    sql = data.get("sql", "")
    # Safety: allow only SELECT statements (educational environment)
    stripped = sql.strip().upper()
    if not stripped.startswith("SELECT"):
        return jsonify({"success": False, "error": "Tylko zapytania SELECT są dozwolone w tej grze.", "columns": [], "rows": []})
    result = query_db(sql)
    return jsonify(result)

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  🔐  SQL INJECTION QUEST  —  Aplikacja edukacyjna")
    print("="*55)
    print("  Otwórz przeglądarkę i wejdź na:")
    print("  ➜  http://localhost:5000")
    print("="*55 + "\n")
    init_db()
    app.run(debug=False, port=5000)