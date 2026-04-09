from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
_db = None

def init_db():
    global _db
    _db = sqlite3.connect("file::memory:?cache=shared", uri=True, check_same_thread=False)
    cur = _db.cursor()
    cur.executescript("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT
        );
        INSERT INTO users VALUES (1,'admin','SuperTajneHaslo123','admin');
        INSERT INTO users VALUES (2,'janek','kot123','user');
        INSERT INTO users VALUES (3,'ania','piesek456','user');
        INSERT INTO users VALUES (4,'bartek','dragon789','user');

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY, name TEXT, price REAL, hidden INTEGER DEFAULT 0
        );
        INSERT INTO products VALUES (1,'Kredki Faber-Castell',19.99,0);
        INSERT INTO products VALUES (2,'Zeszyt A4',3.50,0);
        INSERT INTO products VALUES (3,'Plecak szkolny',89.00,0);
        INSERT INTO products VALUES (4,'🏆 TAJNY SKARB - Złota Odznaka',0.01,1);

        CREATE TABLE IF NOT EXISTS secret_codes (
            id INTEGER PRIMARY KEY, code TEXT, description TEXT
        );
        INSERT INTO secret_codes VALUES (1,'FLAG{SQL_W1Z4RD}','Kod mistrza SQL');
        INSERT INTO secret_codes VALUES (2,'FLAG{H4CK3R_K1D}','Kod hakera');
    """)
    _db.commit()

def run_sql(sql):
    try:
        cur = _db.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        cols = [d[0] for d in cur.description] if cur.description else []
        return {"ok": True, "cols": cols, "rows": rows}
    except Exception as e:
        return {"ok": False, "error": str(e)}

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/api/login", methods=["POST"])
def api_login():
    data = request.get_json()
    username = data.get("username", "")
    password  = data.get("password", "")
    sql = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"success": False, "error": r["error"], "sql": sql})
    if r["rows"]:
        row = r["rows"][0]
        return jsonify({"success": True, "user": {"id": row[0], "username": row[1], "role": row[3]}, "sql": sql, "all_rows": r["rows"], "cols": r["cols"]})
    return jsonify({"success": False, "error": "Nieprawidłowy login lub hasło.", "sql": sql})

@app.route("/api/search", methods=["POST"])
def api_search():
    data = request.get_json()
    query = data.get("q", "")
    sql = f"SELECT id, name, price FROM products WHERE hidden = 0 AND name LIKE '%{query}%'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql})
    return jsonify({"ok": True, "cols": r["cols"], "rows": r["rows"], "sql": sql})

HTML = r"""
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<title>SQL Injection — Tryb Realistyczny</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
<style>
* { box-sizing: border-box; margin: 0; padding: 0; }

body {
  font-family: 'Inter', sans-serif;
  background: #0f1117;
  color: #e2e8f0;
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

/* ── TOP BAR ── */
.topbar {
  background: #1a1d27;
  border-bottom: 1px solid #2d3148;
  padding: 0 20px;
  height: 52px;
  display: flex;
  align-items: center;
  gap: 16px;
  flex-shrink: 0;
  z-index: 50;
}

.topbar-title {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: #7c85a2;
  letter-spacing: 1px;
}

.level-tabs {
  display: flex;
  gap: 4px;
  margin-left: auto;
}

.tab-btn {
  background: none;
  border: 1px solid #2d3148;
  border-radius: 6px;
  color: #7c85a2;
  padding: 5px 14px;
  font-size: 0.8rem;
  font-family: 'Inter', sans-serif;
  cursor: pointer;
  transition: all 0.15s;
}
.tab-btn:hover { border-color: #5b6bab; color: #a8b4d8; }
.tab-btn.active { background: #2d3f7c; border-color: #4a5fa8; color: #e2e8f0; }
.tab-btn.done { border-color: #2a6b4a; color: #4ade80; }
.tab-btn.done.active { background: #1a4032; }

.score {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.8rem;
  color: #f59e0b;
  background: rgba(245,158,11,0.1);
  border: 1px solid rgba(245,158,11,0.25);
  border-radius: 20px;
  padding: 4px 14px;
  margin-left: 12px;
}

/* ── MAIN LAYOUT ── */
.workspace {
  flex: 1;
  display: grid;
  grid-template-columns: 1fr 340px;
  overflow: hidden;
}

/* ── LEFT: APP WINDOW ── */
.app-window {
  display: flex;
  flex-direction: column;
  overflow: hidden;
  position: relative;
}

.browser-bar {
  background: #1e2130;
  border-bottom: 1px solid #2d3148;
  padding: 8px 16px;
  display: flex;
  align-items: center;
  gap: 10px;
  flex-shrink: 0;
}

.browser-dots { display: flex; gap: 6px; }
.browser-dots span {
  width: 11px; height: 11px; border-radius: 50%;
}
.bd-r { background: #ff5f57; }
.bd-y { background: #febc2e; }
.bd-g { background: #28c840; }

.browser-url {
  flex: 1;
  background: #141720;
  border: 1px solid #2d3148;
  border-radius: 6px;
  padding: 5px 12px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #7c85a2;
}

.app-frame {
  flex: 1;
  overflow-y: auto;
  background: #f5f6fa;
  position: relative;
}

/* ── PAGES inside frame ── */
.page { display: none; height: 100%; }
.page.active { display: block; }

/* Login page */
.login-page {
  min-height: 100%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  align-items: center;
  justify-content: center;
}

.login-card {
  background: white;
  border-radius: 16px;
  padding: 40px 44px;
  width: 380px;
  box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.login-logo {
  text-align: center;
  margin-bottom: 28px;
}

.login-logo .logo-icon { font-size: 2.5rem; }
.login-logo h2 { color: #1a1d27; font-size: 1.3rem; font-weight: 700; margin-top: 8px; }
.login-logo p { color: #94a3b8; font-size: 0.85rem; margin-top: 4px; }

.form-group { margin-bottom: 18px; }
.form-group label { display: block; font-size: 0.82rem; font-weight: 600; color: #374151; margin-bottom: 6px; }

.form-group input {
  width: 100%;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 11px 14px;
  font-size: 0.9rem;
  font-family: 'Inter', sans-serif;
  outline: none;
  color: #111;
  transition: border-color 0.2s;
}
.form-group input:focus { border-color: #667eea; }

.login-btn {
  width: 100%;
  background: linear-gradient(135deg, #667eea, #764ba2);
  color: white;
  border: none;
  border-radius: 8px;
  padding: 12px;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  margin-top: 6px;
  transition: opacity 0.2s;
}
.login-btn:hover { opacity: 0.9; }

.login-result {
  margin-top: 16px;
  border-radius: 8px;
  padding: 12px 14px;
  font-size: 0.85rem;
  display: none;
}
.login-result.error { background: #fef2f2; color: #dc2626; border: 1px solid #fecaca; }
.login-result.success { background: #f0fdf4; color: #16a34a; border: 1px solid #bbf7d0; }

/* Shop page */
.shop-page {
  background: #f8fafc;
  min-height: 100%;
}

.shop-nav {
  background: white;
  border-bottom: 1px solid #e5e7eb;
  padding: 0 28px;
  height: 56px;
  display: flex;
  align-items: center;
  gap: 16px;
}

.shop-nav .nav-logo { font-weight: 800; font-size: 1.1rem; color: #1e40af; }
.shop-nav .nav-logo span { color: #f59e0b; }

.search-bar-wrap {
  flex: 1;
  display: flex;
  gap: 8px;
  max-width: 500px;
}

.search-input {
  flex: 1;
  border: 2px solid #e5e7eb;
  border-radius: 8px;
  padding: 8px 14px;
  font-size: 0.88rem;
  font-family: 'Inter', sans-serif;
  outline: none;
  color: #111;
  transition: border-color 0.2s;
}
.search-input:focus { border-color: #1e40af; }

.search-btn {
  background: #1e40af;
  color: white;
  border: none;
  border-radius: 8px;
  padding: 8px 20px;
  font-size: 0.88rem;
  font-weight: 600;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
}

.shop-body { padding: 28px; }
.shop-body h3 { font-size: 1rem; font-weight: 600; color: #374151; margin-bottom: 16px; }

.product-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(180px, 1fr));
  gap: 16px;
}

.product-card {
  background: white;
  border-radius: 12px;
  padding: 20px 16px;
  border: 1px solid #e5e7eb;
  text-align: center;
  transition: box-shadow 0.2s;
}
.product-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.1); }
.product-card .p-icon { font-size: 2rem; margin-bottom: 10px; }
.product-card .p-name { font-size: 0.85rem; font-weight: 600; color: #1f2937; margin-bottom: 6px; }
.product-card .p-price { font-size: 1rem; font-weight: 700; color: #1e40af; }
.product-card.secret { border-color: #f59e0b; background: #fffbeb; }

.search-error {
  background: #fef2f2;
  color: #dc2626;
  border: 1px solid #fecaca;
  border-radius: 8px;
  padding: 10px 14px;
  font-size: 0.85rem;
  margin-bottom: 14px;
  display: none;
}

/* ── RIGHT: HINT PANEL ── */
.hint-panel {
  border-left: 1px solid #2d3148;
  background: #13161f;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.hint-header {
  padding: 14px 18px;
  border-bottom: 1px solid #2d3148;
  font-size: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  color: #7c85a2;
  text-transform: uppercase;
  letter-spacing: 1px;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-shrink: 0;
}

.hint-body {
  flex: 1;
  overflow-y: auto;
  padding: 18px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.hint-section {
  background: #1a1d27;
  border: 1px solid #2d3148;
  border-radius: 10px;
  overflow: hidden;
}

.hint-section-title {
  padding: 10px 14px;
  font-size: 0.72rem;
  font-family: 'JetBrains Mono', monospace;
  color: #7c85a2;
  border-bottom: 1px solid #2d3148;
  text-transform: uppercase;
  letter-spacing: 1px;
}

.hint-section-body {
  padding: 12px 14px;
  font-size: 0.82rem;
  line-height: 1.7;
  color: #94a3b8;
}

.hint-section-body code {
  font-family: 'JetBrains Mono', monospace;
  background: #0d0f18;
  color: #7dd3fc;
  padding: 1px 6px;
  border-radius: 4px;
  font-size: 0.78rem;
}

.sql-reveal {
  background: #0d0f18;
  border: 1px solid #2d3148;
  border-radius: 8px;
  padding: 12px 14px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  line-height: 1.8;
  color: #475569;
  margin-top: 6px;
  word-break: break-all;
}

.sql-reveal .kw { color: #818cf8; }
.sql-reveal .str { color: #86efac; }
.sql-reveal .injected { color: #f87171; font-weight: 600; }
.sql-reveal .dim { color: #334155; }

.locked-hint {
  text-align: center;
  padding: 40px 20px;
  color: #334155;
}
.locked-hint .lock-icon { font-size: 2.5rem; margin-bottom: 12px; }
.locked-hint p { font-size: 0.85rem; line-height: 1.6; }

.success-flash {
  background: rgba(74,222,128,0.08);
  border: 1px solid rgba(74,222,128,0.25);
  border-radius: 10px;
  padding: 14px;
  text-align: center;
  display: none;
}
.success-flash.show { display: block; }
.success-flash h4 { color: #4ade80; font-size: 0.95rem; margin-bottom: 6px; }
.success-flash p { font-size: 0.82rem; color: #64748b; line-height: 1.5; }

/* ── SQL LOG ── */
.sql-log {
  border-top: 1px solid #2d3148;
  padding: 14px 18px;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.72rem;
  color: #334155;
  flex-shrink: 0;
  min-height: 60px;
  max-height: 120px;
  overflow-y: auto;
  background: #0d0f18;
}

.sql-log .log-label { color: #475569; margin-bottom: 4px; }
.sql-log .log-sql { color: #7c85a2; word-break: break-all; line-height: 1.6; }
.sql-log .log-sql .injected { color: #f87171; }

/* scrollbars */
::-webkit-scrollbar { width: 5px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #2d3148; border-radius: 4px; }
</style>
</head>
<body>

<!-- TOP BAR -->
<div class="topbar">
  <div class="topbar-title">🔐 SQL INJECTION — TRYB REALISTYCZNY</div>
  <div class="level-tabs">
    <button class="tab-btn active" onclick="gotoLevel(0)" id="tab0">L1</button>
    <button class="tab-btn" onclick="gotoLevel(1)" id="tab1">L2</button>
    <button class="tab-btn" onclick="gotoLevel(2)" id="tab2">L3</button>
    <button class="tab-btn" onclick="gotoLevel(3)" id="tab3">L4</button>
    <button class="tab-btn" onclick="gotoLevel(4)" id="tab4">L5</button>
  </div>
  <div class="score" id="score">⭐ 0 / 5</div>
</div>

<!-- WORKSPACE -->
<div class="workspace">

  <!-- LEFT: APP WINDOW -->
  <div class="app-window">
    <div class="browser-bar">
      <div class="browser-dots">
        <span class="bd-r"></span><span class="bd-y"></span><span class="bd-g"></span>
      </div>
      <div class="browser-url" id="browserUrl">http://szkolnyportal.pl/login</div>
    </div>

    <div class="app-frame">

      <!-- PAGE 1: Login (only username field) -->
      <div class="page active" id="page0">
        <div class="login-page">
          <div class="login-card">
            <div class="login-logo">
              <div class="logo-icon">🏫</div>
              <h2>Szkolny Portal</h2>
              <p>Zaloguj się do systemu</p>
            </div>
            <div class="form-group">
              <label>Nazwa użytkownika</label>
              <input type="text" id="l0_user" placeholder="wpisz login..." onkeydown="if(e=>e.key==='Enter')document.getElementById('btn0').click()">
            </div>
            <button class="login-btn" id="btn0" onclick="doLogin0()">Zaloguj się →</button>
            <div class="login-result" id="res0"></div>
          </div>
        </div>
      </div>

      <!-- PAGE 2: Login with password too -->
      <div class="page" id="page1">
        <div class="login-page" style="background: linear-gradient(135deg,#0f2027,#203a43,#2c5364)">
          <div class="login-card">
            <div class="login-logo">
              <div class="logo-icon">🔒</div>
              <h2>Panel Administratora</h2>
              <p>Dostęp tylko dla uprawnionych</p>
            </div>
            <div class="form-group">
              <label>Login</label>
              <input type="text" id="l1_user" placeholder="login administratora...">
            </div>
            <div class="form-group">
              <label>Hasło</label>
              <input type="password" id="l1_pass" placeholder="••••••••">
            </div>
            <button class="login-btn" style="background:linear-gradient(135deg,#0f2027,#2c5364)" onclick="doLogin1()">Zaloguj się →</button>
            <div class="login-result" id="res1"></div>
          </div>
        </div>
      </div>

      <!-- PAGE 3: Shop search -->
      <div class="page" id="page2">
        <div class="shop-page">
          <div class="shop-nav">
            <div class="nav-logo">Sklep<span>ABC</span></div>
            <div class="search-bar-wrap">
              <input class="search-input" id="l2_search" placeholder="Szukaj produktu..." onkeydown="if(event.key==='Enter')doSearch2()">
              <button class="search-btn" onclick="doSearch2()">Szukaj</button>
            </div>
          </div>
          <div class="shop-body">
            <div class="search-error" id="err2"></div>
            <h3 id="shop2label">Wpisz nazwę produktu żeby wyszukać</h3>
            <div class="product-grid" id="grid2"></div>
          </div>
        </div>
      </div>

      <!-- PAGE 4: Shop search (UNION attack) -->
      <div class="page" id="page3">
        <div class="shop-page">
          <div class="shop-nav">
            <div class="nav-logo">Sklep<span>ABC</span></div>
            <div class="search-bar-wrap">
              <input class="search-input" id="l3_search" placeholder="Szukaj produktu..." onkeydown="if(event.key==='Enter')doSearch3()">
              <button class="search-btn" onclick="doSearch3()">Szukaj</button>
            </div>
          </div>
          <div class="shop-body">
            <div class="search-error" id="err3"></div>
            <h3 id="shop3label">Wpisz nazwę produktu żeby wyszukać</h3>
            <div class="product-grid" id="grid3"></div>
          </div>
        </div>
      </div>

      <!-- PAGE 5: Shop search (steal password) -->
      <div class="page" id="page4">
        <div class="shop-page">
          <div class="shop-nav">
            <div class="nav-logo">Sklep<span>ABC</span></div>
            <div class="search-bar-wrap">
              <input class="search-input" id="l4_search" placeholder="Szukaj produktu..." onkeydown="if(event.key==='Enter')doSearch4()">
              <button class="search-btn" onclick="doSearch4()">Szukaj</button>
            </div>
          </div>
          <div class="shop-body">
            <div class="search-error" id="err4"></div>
            <h3 id="shop4label">Wpisz nazwę produktu żeby wyszukać</h3>
            <div class="product-grid" id="grid4"></div>
          </div>
        </div>
      </div>

    </div><!-- /app-frame -->
  </div><!-- /app-window -->

  <!-- RIGHT: HINT PANEL -->
  <div class="hint-panel">
    <div class="hint-header">
      <span>💬</span> Panel nauczyciela
    </div>

    <div class="hint-body" id="hintBody">
      <!-- content injected by JS -->
    </div>

    <div class="sql-log" id="sqlLog">
      <div class="log-label">// ostatnie zapytanie SQL:</div>
      <div class="log-sql" id="logSql">— brak —</div>
    </div>
  </div>

</div><!-- /workspace -->

<script>
const HINTS = [
  {
    title: "🔑 Poziom 1 — Wyłam logowanie",
    goal: "Zaloguj się jako admin bez znajomości hasła. Wpisz cokolwiek w pole nazwy użytkownika.",
    hint: true,
    hintText: `Formularz ma <strong>jedno pole</strong> — samą nazwę użytkownika.<br><br>
SQL wygląda tak:<br>
<code>WHERE username = '[TWÓJ INPUT]'</code><br><br>
Spróbuj wpisać:<br>
<code>admin' OR '1'='1</code><br><br>
Apostrof <code>'</code> "wyłamuje" się ze stringa, a <code>OR '1'='1'</code> sprawia że warunek jest zawsze prawdziwy!`,
    url: "http://szkolnyportal.pl/login",
    successMsg: "Brawo! Ominąłeś/ominęłaś sprawdzanie loginu! Apostrof 'wyłamał' się ze stringa SQL."
  },
  {
    title: "🗑️ Poziom 2 — Pomiń hasło",
    goal: "Teraz jest i login i hasło. Zaloguj się jako admin bez żadnego hasła.",
    hint: true,
    hintText: `Teraz SQL sprawdza oba pola:<br>
<code>WHERE username='...' AND password='...'</code><br><br>
W SQL, <code>--</code> to komentarz — reszta linii jest ignorowana!<br><br>
Wpisz w pole loginu:<br>
<code>admin'--</code><br><br>
Część z hasłem znika jak przez magię! ✨<br>
Pole hasła możesz zostawić puste.`,
    url: "http://szkolnyportal.pl/admin",
    successMsg: "Super! Komentarz -- 'wyciął' warunek z hasłem z zapytania SQL!"
  },
  {
    title: "👁️ Poziom 3 — Znajdź ukryty produkt",
    goal: "W sklepie jest tajny produkt oznaczony jako hidden=1. Znajdź go przez wyszukiwarkę!",
    hint: false,
    url: "http://sklepabc.pl/search",
    successMsg: "Świetnie! Ukryty produkt ujawniony! Warunek hidden=0 przestał działać."
  },
  {
    title: "🗂️ Poziom 4 — Połącz tabele (UNION)",
    goal: "W bazie jest ukryta tabela secret_codes. Użyj UNION SELECT żeby ją wyświetlić w wynikach wyszukiwania!",
    hint: false,
    url: "http://sklepabc.pl/search",
    successMsg: "Niesamowite! UNION połączyło dwa zapytania w jedno — dane z innej tabeli pojawiły się w wynikach!"
  },
  {
    title: "👑 Poziom 5 — Wykradnij hasło admina",
    goal: "Finał! Użyj UNION SELECT żeby wyświetlić hasło admina z tabeli users razem z wynikami wyszukiwania.",
    hint: false,
    url: "http://sklepabc.pl/search",
    successMsg: "🏆 MISTRZ! Wykradłeś/wykradłaś hasło admina przez lukę w wyszukiwarce sklepu!"
  }
];

let currentLevel = 0;
let solved = new Set();
let lastSql = "";

// ── LEVEL NAVIGATION ──
function gotoLevel(idx) {
  currentLevel = idx;
  document.querySelectorAll('.page').forEach((p,i) => p.classList.toggle('active', i === idx));
  document.querySelectorAll('.tab-btn').forEach((t,i) => t.classList.toggle('active', i === idx));
  document.getElementById('browserUrl').textContent = HINTS[idx].url;
  renderHintPanel(idx);
}

// ── HINT PANEL ──
function renderHintPanel(idx) {
  const h = HINTS[idx];
  let html = '';

  // Mission card
  html += `<div class="hint-section">
    <div class="hint-section-title">🎯 Cel misji</div>
    <div class="hint-section-body">${h.goal}</div>
  </div>`;

  // Hint (only for early levels)
  if (h.hint) {
    html += `<div class="hint-section">
      <div class="hint-section-title">💡 Wskazówka</div>
      <div class="hint-section-body">${h.hintText}</div>
    </div>`;
  } else {
    html += `<div class="hint-section">
      <div class="hint-section-title">💡 Wskazówka</div>
      <div class="hint-section-body">
        <div class="locked-hint">
          <div class="lock-icon">🔐</div>
          <p>Wskazówka ukryta.<br>Musisz sam(a) odkryć jak to zrobić!</p>
        </div>
      </div>
    </div>`;
  }

  // Success flash
  html += `<div class="success-flash" id="successFlash">
    <h4>✅ Poziom zaliczony!</h4>
    <p>${h.successMsg}</p>
  </div>`;

  document.getElementById('hintBody').innerHTML = html;

  if (solved.has(idx)) {
    document.getElementById('successFlash').classList.add('show');
  }
}

// ── SQL LOG ──
function logSQL(sql, injectedPart) {
  lastSql = sql;
  const el = document.getElementById('logSql');
  // highlight injected part
  if (injectedPart) {
    const escaped = sql.replace(injectedPart, `<span class="injected">${injectedPart}</span>`);
    el.innerHTML = escaped;
  } else {
    el.textContent = sql;
  }
}

// ── LEVEL 1: login (username only) ──
async function doLogin0() {
  const u = document.getElementById('l0_user').value;
  const r = await fetch('/api/login', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({username: u, password: 'ignored_not_checked'})
  });
  // We need a different endpoint; build SQL manually for display
  const res = await fetch('/api/level1', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({username: u})
  });
  const data = await res.json();
  logSQL(data.sql, u);
  const el = document.getElementById('res0');
  el.style.display = 'block';
  if (data.success) {
    el.className = 'login-result success';
    el.innerHTML = `✅ Zalogowano jako: <strong>${data.user.username}</strong> (rola: ${data.user.role})`;
    if (data.user.role === 'admin' || data.all_rows.length > 1) markSolved(0);
  } else {
    el.className = 'login-result error';
    el.textContent = '❌ ' + data.error;
  }
}

// ── LEVEL 2: login (username + password) ──
async function doLogin1() {
  const u = document.getElementById('l1_user').value;
  const p = document.getElementById('l1_pass').value;
  const res = await fetch('/api/login', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({username: u, password: p})
  });
  const data = await res.json();
  logSQL(data.sql, u);
  const el = document.getElementById('res1');
  el.style.display = 'block';
  if (data.success) {
    el.className = 'login-result success';
    el.innerHTML = `✅ Zalogowano jako: <strong>${data.user.username}</strong> (rola: ${data.user.role})`;
    if (data.user.role === 'admin') markSolved(1);
  } else {
    el.className = 'login-result error';
    el.textContent = '❌ ' + data.error;
  }
}

// ── LEVEL 3: shop search (find hidden) ──
async function doSearch2() {
  const q = document.getElementById('l2_search').value;
  const res = await fetch('/api/search', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({q})
  });
  const data = await res.json();
  logSQL(data.sql, q);
  renderShop('grid2','shop2label','err2', data);
  if (data.ok && data.rows.some(r => r[1] && r[1].includes('SKARB'))) markSolved(2);
}

// ── LEVEL 4: UNION attack ──
async function doSearch3() {
  const q = document.getElementById('l3_search').value;
  const res = await fetch('/api/search', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({q})
  });
  const data = await res.json();
  logSQL(data.sql, q);
  renderShop('grid3','shop3label','err3', data);
  if (data.ok && data.rows.some(r => r.some(c => typeof c==='string' && c.includes('FLAG')))) markSolved(3);
}

// ── LEVEL 5: steal password ──
async function doSearch4() {
  const q = document.getElementById('l4_search').value;
  const res = await fetch('/api/search', {
    method:'POST', headers:{'Content-Type':'application/json'},
    body: JSON.stringify({q})
  });
  const data = await res.json();
  logSQL(data.sql, q);
  renderShop('grid4','shop4label','err4', data);
  if (data.ok && data.rows.some(r => r.some(c => typeof c==='string' && c.includes('SuperTajne')))) markSolved(4);
}

// ── RENDER SHOP GRID ──
const icons = ['🖊️','📓','🎒','🏆','💻','📚','🗂️','🔑','💎','⭐'];
function renderShop(gridId, labelId, errId, data) {
  const grid = document.getElementById(gridId);
  const label = document.getElementById(labelId);
  const err = document.getElementById(errId);

  if (!data.ok) {
    err.style.display = 'block';
    err.textContent = '⚠️ Błąd serwera: ' + data.error;
    grid.innerHTML = '';
    label.textContent = 'Błąd wyszukiwania';
    return;
  }
  err.style.display = 'none';

  if (data.rows.length === 0) {
    label.textContent = 'Brak wyników';
    grid.innerHTML = '<p style="color:#94a3b8;font-size:.85rem">Nie znaleziono produktów.</p>';
    return;
  }

  label.textContent = `Znaleziono ${data.rows.length} wynik(i):`;
  grid.innerHTML = data.rows.map((row, i) => {
    const name = row[1] || row[0] || '???';
    const price = typeof row[2] === 'number' ? row[2].toFixed(2) + ' zł' : (row[2] || '');
    const isSecret = name.includes('SKARB') || name.includes('FLAG');
    const icon = icons[i % icons.length];
    return `<div class="product-card ${isSecret ? 'secret' : ''}">
      <div class="p-icon">${icon}</div>
      <div class="p-name">${name}</div>
      <div class="p-price">${price}</div>
    </div>`;
  }).join('');
}

// ── MARK SOLVED ──
function markSolved(idx) {
  solved.add(idx);
  document.getElementById(`tab${idx}`).classList.add('done');
  document.getElementById('score').textContent = `⭐ ${solved.size} / 5`;
  const sf = document.getElementById('successFlash');
  if (sf) sf.classList.add('show');
}

// ── INIT ──
gotoLevel(0);
</script>
</body>
</html>
"""

@app.route("/api/level1", methods=["POST"])
def api_level1():
    """Level 1 - only username check"""
    data = request.get_json()
    username = data.get("username", "")
    sql = f"SELECT * FROM users WHERE username = '{username}'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"success": False, "error": r["error"], "sql": sql})
    if r["rows"]:
        row = r["rows"][0]
        return jsonify({"success": True, "user": {"id": row[0], "username": row[1], "role": row[3]},
                        "sql": sql, "all_rows": r["rows"], "cols": r["cols"]})
    return jsonify({"success": False, "error": "Nie znaleziono użytkownika.", "sql": sql})

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  🔐  SQL INJECTION QUEST — Tryb Realistyczny")
    print("="*55)
    print("  Otwórz przeglądarkę i wejdź na:")
    print("  ➜  http://localhost:5001")
    print("="*55 + "\n")
    init_db()
    app.run(debug=False, port=5001)