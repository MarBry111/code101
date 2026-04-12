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
        INSERT INTO users VALUES (1,'admin','H@slo_Admina_2024!','admin');
        INSERT INTO users VALUES (2,'janek','kotek123','user');
        INSERT INTO users VALUES (3,'ania','piesek456','user');
        INSERT INTO users VALUES (4,'bartek','dragon789','user');

        -- Sklep (poziom 2): 3 kolumny w SELECT: id, name, price
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY, name TEXT, price REAL
        );
        INSERT INTO products VALUES (1,'Dlugopis Parker',29.99);
        INSERT INTO products VALUES (2,'Zeszyt A5',4.50);
        INSERT INTO products VALUES (3,'Plecak Nike',159.00);
        INSERT INTO products VALUES (4,'Kalkulator Casio',49.00);

        -- Blog (poziom 4): 3 kolumny w SELECT: id, title, content
        CREATE TABLE IF NOT EXISTS articles (
            id INTEGER PRIMARY KEY, title TEXT, content TEXT, author TEXT
        );
        INSERT INTO articles VALUES (1,'Jak sie uczyc SQL','SQL to jezyk baz danych...','Jan Kowalski');
        INSERT INTO articles VALUES (2,'Python dla poczatkujacych','Python jest prosty i potezny...','Anna Nowak');
        INSERT INTO articles VALUES (3,'Cyberbezpieczenstwo w szkole','Chronmy swoje dane...','Tomasz Wisniewski');

        -- Kody tajne (cel dla L4): te same 3 kolumny co articles
        CREATE TABLE IF NOT EXISTS secret_codes (
            id INTEGER PRIMARY KEY, code TEXT, description TEXT
        );
        INSERT INTO secret_codes VALUES (1,'FLAG{UNION_M4ST3R}','Kod dla mistrza UNION');
        INSERT INTO secret_codes VALUES (2,'FLAG{SQL_H4CK3R}','Kod hakera SQL');

        -- Przesylki (poziom 5): 4 kolumny w SELECT
        CREATE TABLE IF NOT EXISTS packages (
            id INTEGER PRIMARY KEY,
            tracking_id TEXT, status TEXT, destination TEXT, estimated TEXT
        );
        INSERT INTO packages VALUES (1,'PKG-001','W drodze','Warszawa, ul. Kwiatowa 5','2024-12-20');
        INSERT INTO packages VALUES (2,'PKG-002','Dostarczona','Krakow, ul. Dluga 12','2024-12-18');
        INSERT INTO packages VALUES (3,'PKG-003','W sortowni','Gdansk, ul. Morska 3','2024-12-21');
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

# ══ L1: Tutorial ══════════════════════════════════════
# SELECT * FROM users WHERE username = '{input}'
# Technika: ' OR '1'='1
# Wygrana: zwrocono wiecej niz 1 uzytkownika
@app.route("/api/l1", methods=["POST"])
def l1():
    d = request.get_json()
    u = d.get("u", "")
    sql = f"SELECT id, username, role FROM users WHERE username = '{u}'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql, "rows": []})
    return jsonify({"ok": True, "sql": sql, "rows": r["rows"], "cols": r["cols"]})

# ══ L2: E-sklep, ID numeryczne ════════════════════════
# SELECT id, name, price FROM products WHERE id = {input}  ← BRAK APOSTROFOW
# Technika: 0 UNION SELECT id, username, password FROM users--
# Wygrana: haslo admina widoczne w wynikach jako "cena"
@app.route("/api/l2", methods=["POST"])
def l2():
    d = request.get_json()
    pid = d.get("id", "1")
    # Liczba bez apostrofow - celowo podatne
    sql = f"SELECT id, name, price FROM products WHERE id = {pid}"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql, "rows": []})
    return jsonify({"ok": True, "sql": sql, "rows": r["rows"], "cols": r["cols"]})

# ══ L3: Panel admina, login + haslo ══════════════════
# SELECT * FROM users WHERE username='{u}' AND password='{p}'
# Technika: admin'-- (komentarz ustrzeluje warunek z haslem)
@app.route("/api/l3", methods=["POST"])
def l3():
    d = request.get_json()
    u = d.get("u", "")
    p = d.get("p", "")
    sql = f"SELECT id, username, role FROM users WHERE username = '{u}' AND password = '{p}'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql})
    if r["rows"] and r["rows"][0][2] == "admin":
        return jsonify({"ok": True, "user": r["rows"][0][1], "role": r["rows"][0][2], "sql": sql})
    if r["rows"]:
        return jsonify({"ok": False, "error": "Brak uprawnien administratora.", "sql": sql})
    return jsonify({"ok": False, "error": "Nieprawidlowy login lub haslo.", "sql": sql})

# ══ L4: Blog, wyszukiwarka artykulow ══════════════════
# SELECT id, title, content FROM articles WHERE title LIKE '%{q}%'
# Technika: ' UNION SELECT id,code,description FROM secret_codes--
# UWAGA: 3 kolumny musza sie zgadzac!
@app.route("/api/l4", methods=["POST"])
def l4():
    d = request.get_json()
    q = d.get("q", "")
    sql = f"SELECT id, title, content FROM articles WHERE title LIKE '%{q}%'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql, "rows": []})
    return jsonify({"ok": True, "sql": sql, "rows": r["rows"], "cols": r["cols"]})

# ══ L5: Sledzenie przesylek ════════════════════════════
# SELECT tracking_id, status, destination, estimated FROM packages WHERE tracking_id = '{input}'
# Technika: ' UNION SELECT username, password, role, id FROM users WHERE role='admin'--
# UWAGA: 4 kolumny! Inne niz w poprzednich poziomach.
@app.route("/api/l5", methods=["POST"])
def l5():
    d = request.get_json()
    tid = d.get("id", "")
    sql = f"SELECT tracking_id, status, destination, estimated FROM packages WHERE tracking_id = '{tid}'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql, "rows": []})
    return jsonify({"ok": True, "sql": sql, "rows": r["rows"], "cols": r["cols"]})

# ══════════════════════════════════════════════════════
HTML = r"""
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<title>SQL Injection Quest</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#0d1117;color:#e2e8f0;height:100vh;display:flex;flex-direction:column;overflow:hidden}

/* TOPBAR */
.topbar{background:#161b22;border-bottom:1px solid #21262d;padding:0 18px;height:48px;display:flex;align-items:center;gap:12px;flex-shrink:0}
.tbtitle{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:#58a6ff;letter-spacing:1px}
.tabs{display:flex;gap:3px;margin-left:auto}
.tab{background:none;border:1px solid #30363d;border-radius:6px;color:#8b949e;padding:4px 12px;font-size:.75rem;font-family:'Inter',sans-serif;cursor:pointer;transition:all .15s;white-space:nowrap}
.tab:hover{border-color:#58a6ff;color:#cdd9e5}
.tab.active{background:#1f3558;border-color:#388bfd;color:#e2e8f0}
.tab.done{border-color:#238636;color:#3fb950}
.tab.done.active{background:#0d2b1f;border-color:#3fb950}
.score{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:#d29922;background:rgba(210,153,34,.1);border:1px solid rgba(210,153,34,.3);border-radius:20px;padding:4px 12px;margin-left:8px}

/* LAYOUT */
.workspace{flex:1;display:grid;grid-template-columns:1fr 370px;overflow:hidden}

/* LEFT: APP WINDOW */
.appwin{display:flex;flex-direction:column;overflow:hidden;border-right:1px solid #21262d}
.chromebar{background:#1c2128;border-bottom:1px solid #21262d;padding:7px 14px;display:flex;align-items:center;gap:10px;flex-shrink:0}
.dots{display:flex;gap:5px}
.dots span{width:10px;height:10px;border-radius:50%}
.dr{background:#ff5f56}.dy{background:#ffbd2e}.dg{background:#27c93f}
.urlbar{flex:1;background:#0d1117;border:1px solid #30363d;border-radius:5px;padding:4px 12px;font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#8b949e}
.frame{flex:1;overflow-y:auto}
.pg{display:none;min-height:100%}
.pg.active{display:block}

/* ── L1: Tutorial login ── */
.tut-wrap{min-height:100%;background:#f0f2f5;display:flex;flex-direction:column;align-items:center;padding:30px 20px;gap:20px}
.tut-card{background:white;border-radius:12px;box-shadow:0 2px 16px rgba(0,0,0,.1);width:100%;max-width:440px;overflow:hidden}
.tut-card-header{background:#4f46e5;padding:20px 24px}
.tut-card-header h2{color:white;font-size:1.1rem;font-weight:700}
.tut-card-header p{color:rgba(255,255,255,.7);font-size:.8rem;margin-top:3px}
.tut-card-body{padding:20px 24px}
.fg{margin-bottom:14px}
.fg label{display:block;font-size:.78rem;font-weight:600;color:#374151;margin-bottom:5px}
.fg input{width:100%;border:1.5px solid #e5e7eb;border-radius:7px;padding:9px 12px;font-size:.88rem;font-family:'Inter',sans-serif;outline:none;color:#111;transition:border-color .2s}
.fg input:focus{border-color:#4f46e5}
.lbtn{width:100%;border:none;border-radius:8px;padding:10px;font-size:.88rem;font-weight:700;cursor:pointer;font-family:'Inter',sans-serif;color:white;transition:opacity .2s}
.lbtn:hover{opacity:.88}
.lresult{margin-top:12px;border-radius:7px;padding:9px 12px;font-size:.82rem;display:none}
.lresult.err{background:#fef2f2;color:#dc2626;border:1px solid #fecaca}
.lresult.ok{background:#f0fdf4;color:#16a34a;border:1px solid #bbf7d0}

/* Live SQL preview (only in L1) */
.sql-preview{background:white;border-radius:12px;box-shadow:0 2px 16px rgba(0,0,0,.1);width:100%;max-width:440px;overflow:hidden}
.sql-preview-hdr{background:#1e1e2e;padding:10px 16px;display:flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#6272a4}
.sql-preview-hdr .badge{background:#50fa7b;color:#1e1e2e;border-radius:4px;padding:1px 7px;font-size:.65rem;font-weight:700}
.sql-preview-body{background:#282a36;padding:14px 16px;font-family:'JetBrains Mono',monospace;font-size:.78rem;line-height:1.9;word-break:break-all}
.kw{color:#ff79c6}.fn{color:#8be9fd}.str{color:#f1fa8c}.inj{color:#ff5555;font-weight:700;text-decoration:underline;text-underline-offset:2px}.dim{color:#6272a4}
.sql-result-tbl{width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:.75rem;margin-top:10px}
.sql-result-tbl th{background:#44475a;color:#f8f8f2;padding:6px 10px;text-align:left}
.sql-result-tbl td{padding:6px 10px;border-bottom:1px solid #383a4a;color:#f8f8f2}

/* ── L2: E-sklep ── */
.shop{background:#f8fafc;min-height:100%}
.shopnav{background:white;border-bottom:1px solid #e5e7eb;padding:0 20px;height:52px;display:flex;align-items:center;gap:14px;position:sticky;top:0;z-index:10}
.shopbrand{font-weight:900;font-size:1.1rem;color:#7c3aed}
.shopbrand span{color:#f59e0b}
.shopnav-right{margin-left:auto;display:flex;align-items:center;gap:8px;font-size:.82rem;color:#6b7280}
.shopnav-right input{border:1.5px solid #e5e7eb;border-radius:7px;padding:6px 10px;font-size:.82rem;font-family:'Inter',sans-serif;width:70px;outline:none;color:#111}
.shopnav-right input:focus{border-color:#7c3aed}
.shopnav-right button{background:#7c3aed;color:white;border:none;border-radius:7px;padding:6px 14px;font-size:.82rem;font-weight:600;cursor:pointer}
.shopbody{padding:20px}
.shopgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(150px,1fr));gap:12px;margin-top:12px}
.scard{background:white;border-radius:10px;padding:16px 12px;border:1px solid #e5e7eb;text-align:center;transition:box-shadow .2s}
.scard:hover{box-shadow:0 4px 14px rgba(0,0,0,.08)}
.scard.alert{border-color:#ef4444;background:#fef2f2}
.scard .sico{font-size:1.6rem;margin-bottom:8px}
.scard .snm{font-size:.78rem;font-weight:600;color:#111;margin-bottom:4px}
.scard .spr{font-size:.9rem;font-weight:700;color:#7c3aed}
.sherr{background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:7px;padding:8px 12px;font-size:.8rem;margin-bottom:10px;display:none}

/* ── L3: Admin panel ── */
.adminbg{min-height:100%;background:linear-gradient(135deg,#0f172a 0%,#1e1b4b 100%);display:flex;align-items:center;justify-content:center;padding:40px 20px}
.admincard{background:#1e2235;border:1px solid #2d3555;border-radius:14px;padding:36px 40px;width:360px;box-shadow:0 20px 60px rgba(0,0,0,.5)}
.admincard .logo{text-align:center;margin-bottom:24px}
.admincard .logo .ico{font-size:2rem}
.admincard .logo h2{color:#e2e8f0;font-size:1.1rem;font-weight:700;margin-top:8px}
.admincard .logo p{color:#64748b;font-size:.78rem;margin-top:3px}
.admincard .fg label{color:#94a3b8}
.admincard .fg input{background:#0f172a;border-color:#2d3555;color:#e2e8f0}
.admincard .fg input:focus{border-color:#6366f1}
.admincard .lbtn{background:linear-gradient(135deg,#6366f1,#8b5cf6)}
.admincard .lresult.err{background:#2d1515;color:#f87171;border-color:#7f1d1d}
.admincard .lresult.ok{background:#0d2b1a;color:#4ade80;border-color:#14532d}
.admin-warning{background:#291a04;border:1px solid #78350f;border-radius:8px;padding:10px 14px;font-size:.75rem;color:#fbbf24;margin-bottom:18px;display:flex;align-items:center;gap:8px}

/* ── L4: Blog / portal ── */
.blog{background:#f9fafb;min-height:100%}
.blognav{background:white;border-bottom:1px solid #e5e7eb;padding:0 20px;height:52px;display:flex;align-items:center;gap:14px;position:sticky;top:0;z-index:10}
.blognav .brand{font-weight:800;font-size:1rem;color:#111}
.blognav .brand span{color:#ef4444}
.blogsearch{display:flex;gap:6px;margin-left:auto}
.blogsearch input{border:1.5px solid #e5e7eb;border-radius:7px;padding:6px 12px;font-size:.83rem;font-family:'Inter',sans-serif;width:180px;outline:none;color:#111}
.blogsearch input:focus{border-color:#111}
.blogsearch button{background:#111;color:white;border:none;border-radius:7px;padding:6px 14px;font-size:.82rem;font-weight:600;cursor:pointer}
.blogbody{padding:20px 24px}
.blogbody h3{font-size:.85rem;font-weight:600;color:#6b7280;margin-bottom:14px}
.article{background:white;border-radius:10px;border:1px solid #e5e7eb;padding:16px 18px;margin-bottom:10px}
.article.flag{border-color:#f59e0b;background:#fffbeb}
.article .atitle{font-size:.95rem;font-weight:700;color:#111;margin-bottom:5px}
.article .acontent{font-size:.82rem;color:#6b7280;line-height:1.6}
.article .ameta{font-size:.72rem;color:#9ca3af;margin-top:8px}
.blogerr{background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:7px;padding:8px 12px;font-size:.8rem;margin-bottom:12px;display:none}

/* ── L5: Kurier / tracking ── */
.courier{background:#f0f4f8;min-height:100%}
.couriernav{background:#1a56db;padding:0 20px;height:52px;display:flex;align-items:center;gap:10px}
.couriernav .brand{font-weight:800;font-size:1rem;color:white;letter-spacing:1px}
.couriernav .brand span{opacity:.7}
.trackform{max-width:500px;margin:30px auto 0;background:white;border-radius:12px;padding:24px 28px;box-shadow:0 4px 20px rgba(0,0,0,.1)}
.trackform h3{font-size:1rem;font-weight:700;color:#111;margin-bottom:6px}
.trackform p{font-size:.82rem;color:#6b7280;margin-bottom:16px}
.trackinput-row{display:flex;gap:8px}
.trackinput{flex:1;border:2px solid #e5e7eb;border-radius:8px;padding:10px 14px;font-size:.9rem;font-family:'JetBrains Mono',monospace;outline:none;color:#111;letter-spacing:1px;text-transform:uppercase}
.trackinput:focus{border-color:#1a56db}
.trackbtn{background:#1a56db;color:white;border:none;border-radius:8px;padding:10px 20px;font-size:.88rem;font-weight:700;cursor:pointer;font-family:'Inter',sans-serif}
.trackresult{margin-top:20px}
.pkgcard{background:#f8fafc;border-radius:10px;border:1px solid #e5e7eb;padding:16px;margin-bottom:10px}
.pkgcard.alert{border-color:#ef4444;background:#fef2f2}
.pkgcard .pkgid{font-family:'JetBrains Mono',monospace;font-size:.8rem;color:#64748b;margin-bottom:6px}
.pkgcard .pkgstatus{font-size:.95rem;font-weight:700;color:#111;margin-bottom:4px}
.pkgcard .pkgdet{font-size:.8rem;color:#6b7280}
.trackerr{background:#fef2f2;color:#dc2626;border:1px solid #fecaca;border-radius:8px;padding:10px 14px;font-size:.82rem;margin-top:14px;display:none}
.trackempty{text-align:center;padding:30px;color:#9ca3af;font-size:.85rem}

/* RIGHT PANEL */
.panel{display:flex;flex-direction:column;overflow:hidden;background:#161b22}
.panel-hdr{padding:11px 16px;border-bottom:1px solid #21262d;font-size:.7rem;font-family:'JetBrains Mono',monospace;color:#8b949e;text-transform:uppercase;letter-spacing:1px;flex-shrink:0}
.panel-body{flex:1;overflow-y:auto;padding:14px;display:flex;flex-direction:column;gap:11px}
.pc{background:#1c2128;border:1px solid #21262d;border-radius:9px;overflow:hidden}
.pc-hdr{padding:8px 12px;font-size:.68rem;font-family:'JetBrains Mono',monospace;color:#8b949e;border-bottom:1px solid #21262d;text-transform:uppercase;letter-spacing:1px}
.pc-body{padding:11px 12px;font-size:.8rem;line-height:1.75;color:#8b949e}
.pc-body code{font-family:'JetBrains Mono',monospace;background:#0d1117;color:#79c0ff;padding:1px 5px;border-radius:4px;font-size:.74rem}
.pc-body strong{color:#cdd9e5}
.tbadge{display:inline-block;background:rgba(56,139,253,.12);border:1px solid rgba(56,139,253,.3);color:#79c0ff;border-radius:5px;padding:2px 8px;font-size:.7rem;font-family:'JetBrains Mono',monospace;margin-bottom:9px}
.warn-badge{background:rgba(245,158,11,.1);border:1px solid rgba(245,158,11,.3);color:#f59e0b;border-radius:5px;padding:2px 8px;font-size:.7rem;font-family:'JetBrains Mono',monospace;display:inline-block;margin-top:4px}
.locked{text-align:center;padding:24px 14px}
.locked .lico{font-size:1.8rem;margin-bottom:8px}
.locked p{font-size:.8rem;line-height:1.6;color:#484f58}
.suc{background:rgba(63,185,80,.07);border:1px solid rgba(63,185,80,.25);border-radius:9px;padding:13px;text-align:center;display:none}
.suc.show{display:block}
.suc h4{color:#3fb950;font-size:.88rem;margin-bottom:5px}
.suc p{font-size:.78rem;color:#8b949e;line-height:1.55}

/* SQL LOG */
.sqllog{border-top:1px solid #21262d;padding:9px 14px;font-family:'JetBrains Mono',monospace;font-size:.68rem;flex-shrink:0;min-height:52px;max-height:90px;overflow-y:auto;background:#0d1117}
.sqllog .lbl{color:#484f58;margin-bottom:3px}
.sqllog .sqltxt{color:#6e7681;word-break:break-all;line-height:1.65}
.sqltxt .inj{color:#f85149;font-weight:700}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-thumb{background:#21262d;border-radius:4px}
</style>
</head>
<body>

<!-- TOPBAR -->
<div class="topbar">
  <div class="tbtitle">🔐 SQL INJECTION QUEST</div>
  <div class="tabs">
    <button class="tab active" onclick="go(0)" id="t0">🎓 Tutorial</button>
    <button class="tab" onclick="go(1)" id="t1">🛒 Sklep</button>
    <button class="tab" onclick="go(2)" id="t2">🔒 Admin</button>
    <button class="tab" onclick="go(3)" id="t3">📰 Blog</button>
    <button class="tab" onclick="go(4)" id="t4">📦 Kurier</button>
  </div>
  <div class="score" id="score">⭐ 0 / 5</div>
</div>

<div class="workspace">

<!-- ══════════ LEFT ══════════ -->
<div class="appwin">
  <div class="chromebar">
    <div class="dots"><span class="dr"></span><span class="dy"></span><span class="dg"></span></div>
    <div class="urlbar" id="urlbar">http://szkolnyportal.pl/login</div>
  </div>
  <div class="frame">

    <!-- ── PAGE 0: Tutorial ── -->
    <div class="pg active" id="pg0">
      <div class="tut-wrap">
        <div class="tut-card">
          <div class="tut-card-header">
            <h2>🏫 Szkolny Portal — logowanie</h2>
            <p>Wpisz swoją nazwę użytkownika</p>
          </div>
          <div class="tut-card-body">
            <div class="fg">
              <label>Nazwa użytkownika</label>
              <input id="l1u" type="text" placeholder="np. janek" oninput="previewSQL()" onkeydown="if(event.key==='Enter')do1()">
            </div>
            <button class="lbtn" style="background:#4f46e5" onclick="do1()">Wejdź →</button>
            <div class="lresult" id="r1"></div>
          </div>
        </div>

        <!-- Live SQL preview -->
        <div class="sql-preview">
          <div class="sql-preview-hdr">
            <span class="badge">DEBUG MODE</span>
            <span>zapytanie SQL budowane na żywo</span>
          </div>
          <div class="sql-preview-body" id="sqlprev">
            <span class="kw">SELECT</span> id, username, role
            <span class="kw">FROM</span> users
            <span class="kw">WHERE</span> username = <span class="str">''</span>
          </div>
          <div style="padding:0 16px 12px" id="l1rows"></div>
        </div>
      </div>
    </div>

    <!-- ── PAGE 1: E-sklep (numeric) ── -->
    <div class="pg" id="pg1">
      <div class="shop">
        <div class="shopnav">
          <div class="shopbrand">Sklep<span>MAX</span></div>
          <div style="flex:1"></div>
          <div class="shopnav-right">
            <span>Produkt #</span>
            <input id="l2id" type="text" value="1" onkeydown="if(event.key==='Enter')do2()">
            <button onclick="do2()">Pokaż</button>
          </div>
        </div>
        <div class="shopbody">
          <div class="sherr" id="e2"></div>
          <div style="font-size:.83rem;color:#6b7280" id="lbl2">Wpisz numer produktu w pasku nawigacji</div>
          <div class="shopgrid" id="g2"></div>
        </div>
      </div>
    </div>

    <!-- ── PAGE 2: Admin panel ── -->
    <div class="pg" id="pg2">
      <div class="adminbg">
        <div class="admincard">
          <div class="logo">
            <div class="ico">🏛️</div>
            <h2>Panel CMS — Administrator</h2>
            <p>Dostęp tylko dla uprawnionych osób</p>
          </div>
          <div class="admin-warning">⚠️ Nieautoryzowany dostęp jest zabroniony</div>
          <div class="fg">
            <label style="color:#94a3b8;font-size:.78rem;font-weight:600;display:block;margin-bottom:5px">Login</label>
            <input id="l3u" type="text" placeholder="login..." style="background:#0f172a;border:1.5px solid #2d3555;border-radius:7px;padding:9px 12px;width:100%;font-size:.88rem;font-family:'Inter',sans-serif;outline:none;color:#e2e8f0" onkeydown="if(event.key==='Enter')do3()">
          </div>
          <div class="fg" style="margin-top:14px">
            <label style="color:#94a3b8;font-size:.78rem;font-weight:600;display:block;margin-bottom:5px">Hasło</label>
            <input id="l3p" type="password" placeholder="••••••••" style="background:#0f172a;border:1.5px solid #2d3555;border-radius:7px;padding:9px 12px;width:100%;font-size:.88rem;font-family:'Inter',sans-serif;outline:none;color:#e2e8f0" onkeydown="if(event.key==='Enter')do3()">
          </div>
          <button class="lbtn" style="background:linear-gradient(135deg,#6366f1,#8b5cf6);margin-top:8px" onclick="do3()">Zaloguj →</button>
          <div class="lresult" id="r3"></div>
        </div>
      </div>
    </div>

    <!-- ── PAGE 3: Blog ── -->
    <div class="pg" id="pg3">
      <div class="blog">
        <div class="blognav">
          <div class="brand">Tech<span>Portal</span></div>
          <div style="font-size:.8rem;color:#6b7280;display:flex;gap:14px;margin-left:16px">
            <span>Aktualności</span><span>Tutoriale</span><span>Forum</span>
          </div>
          <div class="blogsearch">
            <input id="l4q" type="text" placeholder="Szukaj artykułu..." onkeydown="if(event.key==='Enter')do4()">
            <button onclick="do4()">Szukaj</button>
          </div>
        </div>
        <div class="blogbody">
          <div class="blogerr" id="e4"></div>
          <div style="font-size:.85rem;color:#6b7280;margin-bottom:12px" id="lbl4">Wyszukaj artykuł używając pola powyżej</div>
          <div id="arts"></div>
        </div>
      </div>
    </div>

    <!-- ── PAGE 4: Kurier ── -->
    <div class="pg" id="pg4">
      <div class="courier">
        <div class="couriernav">
          <div class="brand">SWIFT<span>EX</span></div>
          <div style="margin-left:auto;font-size:.78rem;color:rgba(255,255,255,.6)">Śledzenie przesyłek</div>
        </div>
        <div style="padding:20px">
          <div class="trackform">
            <h3>Śledź swoją przesyłkę</h3>
            <p>Podaj numer nadania z listu przewozowego</p>
            <div class="trackinput-row">
              <input class="trackinput" id="l5id" type="text" placeholder="PKG-001" onkeydown="if(event.key==='Enter')do5()">
              <button class="trackbtn" onclick="do5()">Sprawdź</button>
            </div>
            <div style="margin-top:8px;font-size:.72rem;color:#9ca3af">Przykłady: PKG-001, PKG-002, PKG-003</div>
            <div class="trackerr" id="e5"></div>
            <div class="trackresult" id="tr5"></div>
          </div>
        </div>
      </div>
    </div>

  </div><!-- /frame -->
</div><!-- /appwin -->

<!-- ══════════ RIGHT PANEL ══════════ -->
<div class="panel">
  <div class="panel-hdr">💬 opis zadania</div>
  <div class="panel-body" id="pb"></div>
  <div class="sqllog">
    <div class="lbl">// zapytanie SQL wysłane do bazy:</div>
    <div class="sqltxt" id="sqlog">— brak —</div>
  </div>
</div>

</div><!-- /workspace -->

<script>
const URLS = [
  'http://szkolnyportal.pl/login',
  'http://sklepmax.pl/produkt?id=1',
  'http://cms-panel.firmaxyz.pl/admin',
  'http://techportal.pl/search?q=',
  'http://swiftex.pl/tracking'
];

const LEVELS = [
  {
    title: '🎓 Poziom 1 — Tutorial: Rozbij formularz logowania',
    badge: "' OR '1'='1",
    goal: `Ten poziom jest <strong>przezroczysty</strong> — widzisz na żywo jak buduje się zapytanie SQL.<br><br>
Formularz szuka użytkownika wpisując Twój tekst dosłownie do SQL.<br>
Spróbuj wpisać <code>janek</code> — zobaczysz co się dzieje.<br><br>
Teraz wpisz: <code>' OR '1'='1</code><br>
Obserwuj jak zmienia się zapytanie i co zwraca baza!`,
    hint: `Apostrof <code>'</code> "wyrywa się" ze stringa i zamyka go. Potem <code>OR '1'='1</code> dokłada warunek który jest <strong>zawsze prawdziwy</strong>.<br><br>
Zapytanie zamiast szukać jednego usera — zwraca <strong>WSZYSTKICH</strong>.`,
    showHint: true,
    success: "Brawo! Widziałeś/widziałaś na żywo jak apostrof łamie SQL. Zamiast 1 użytkownika — baza zwróciła wszystkich!"
  },
  {
    title: '🛒 Poziom 2 — Sklep: Wstrzyknięcie liczbowe',
    badge: "UNION SELECT (bez apostrofów)",
    goal: `Sklep pokazuje produkty po numerze ID. Wpisz <code>1</code>, <code>2</code>, <code>3</code>, <code>4</code> — zobaczysz normalne produkty.<br><br>
<strong>Trik:</strong> SQL tego sklepu wygląda tak:<br>
<code>WHERE id = {twój input}</code><br><br>
Brak apostrofów! Liczby wstrzykuje się <strong>bez</strong> <code>'</code> ani <code>--</code>.<br><br>
Twoim celem: wyświetl hasło admina w miejscu nazwy i ceny produktu, używając UNION SELECT.`,
    hint: null,
    showHint: false,
    success: "Świetnie! Wstrzyknięcie liczbowe nie potrzebuje apostrofów — i dlatego jest szczególnie trudne do wykrycia!"
  },
  {
    title: '🔒 Poziom 3 — Panel admina: Komentarz SQL',
    badge: "admin'--",
    goal: `Panel CMS sprawdza i login, i hasło razem w jednym zapytaniu:<br>
<code>WHERE username='X' AND password='Y'</code><br><br>
Znasz login admina: <code>admin</code>. Hasła nie znasz.<br><br>
W SQL istnieje specjalny symbol który sprawia że <strong>reszta zapytania jest ignorowana</strong>.<br>
Czy potrafisz go znaleźć i wykorzystać?`,
    hint: null,
    showHint: false,
    success: "Dobrze! Komentarz -- 'wyciął' warunek z hasłem. To klasyczna technika — i to JEDYNE zadanie gdzie -- jest odpowiedzią!"
  },
  {
    title: '📰 Poziom 4 — Blog: UNION SELECT (3 kolumny)',
    badge: "UNION SELECT 3 kolumny",
    goal: `Wyszukiwarka bloga przeszukuje artykuły:<br>
<code>SELECT id, title, content FROM articles WHERE title LIKE '%{q}%'</code><br><br>
W bazie jest ukryta tabela <code>secret_codes</code> z kolumnami <code>id, code, description</code>.<br><br>
Użyj UNION SELECT żeby jej zawartość pojawiła się wśród artykułów.<br>
<strong>Uwaga:</strong> UNION wymaga dokładnie tej samej liczby kolumn co oryginał — tutaj <strong>3</strong>.`,
    hint: null,
    showHint: false,
    success: "Niesamowite! UNION połączył dwa zapytania — tajne kody pojawiły się jako 'artykuły' na blogu!"
  },
  {
    title: '📦 Poziom 5 — Kurier: UNION SELECT (4 kolumny!)',
    badge: "UNION SELECT 4 kolumny",
    goal: `System śledzenia przesyłek używa <strong>4 kolumn</strong>:<br>
<code>SELECT tracking_id, status, destination, estimated FROM packages WHERE tracking_id = '{id}'</code><br><br>
Spróbuj najpierw <code>PKG-001</code> żeby zobaczyć jak działa normalnie.<br><br>
Twoim celem: wyświetl dane z tabeli <code>users</code> — ale tym razem musisz dopasować <strong>4 kolumny</strong>.<br>
Tabela users: <code>id, username, password, role</code>`,
    hint: null,
    showHint: false,
    success: "🏆 MISTRZ SQL INJECTION! UNION z 4 kolumnami — dane użytkowników pojawiły się jako 'przesyłki kurierskie'!"
  }
];

let cur = 0;
const solved = new Set();

function go(idx) {
  cur = idx;
  document.querySelectorAll('.pg').forEach((p,i) => p.classList.toggle('active', i===idx));
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.toggle('active', i===idx));
  document.getElementById('urlbar').textContent = URLS[idx];
  renderPanel(idx);
}

function renderPanel(idx) {
  const lv = LEVELS[idx];
  let html = `
    <div class="pc">
      <div class="pc-hdr">🎯 cel misji</div>
      <div class="pc-body">${lv.goal}</div>
    </div>
    <div class="pc">
      <div class="pc-hdr">🔧 technika</div>
      <div class="pc-body">
        <div class="tbadge">${lv.badge}</div><br>
        ${lv.showHint && lv.hint
          ? lv.hint
          : lv.showHint
            ? ''
            : `<div class="locked"><div class="lico">🔐</div><p>Odkryj technikę samodzielnie!<br>Wskazówka ukryta.</p></div>`}
      </div>
    </div>
    <div class="suc ${solved.has(idx)?'show':''}" id="sc${idx}">
      <h4>✅ Poziom zaliczony!</h4>
      <p>${lv.success}</p>
    </div>`;
  document.getElementById('pb').innerHTML = html;
}

function setSQL(sql, inj) {
  const el = document.getElementById('sqlog');
  const e = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  if (inj && sql.includes(inj)) {
    el.innerHTML = e(sql).replace(e(inj), `<span class="inj">${e(inj)}</span>`);
  } else {
    el.textContent = sql;
  }
}

function markSolved(idx) {
  if (solved.has(idx)) return;
  solved.add(idx);
  document.getElementById(`t${idx}`).classList.add('done');
  document.getElementById('score').textContent = `⭐ ${solved.size} / 5`;
  const s = document.getElementById(`sc${idx}`);
  if (s) s.classList.add('show');
}

// ── L1: Tutorial z live preview ──
function previewSQL() {
  const u = document.getElementById('l1u').value;
  const e = s => s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const eu = e(u);
  // highlight injection characters
  const colored = eu
    .replace(/&#x27;/g, "<span class='inj'>'</span>")
    .replace(/'/g, "<span class='inj'>'</span>")
    .replace(/--/g, "<span class='inj'>--</span>")
    .replace(/OR/gi, "<span style='color:#ffb86c'>OR</span>")
    .replace(/UNION/gi, "<span style='color:#ffb86c'>UNION</span>")
    .replace(/SELECT/gi, "<span style='color:#ff79c6'>SELECT</span>");
  document.getElementById('sqlprev').innerHTML =
    `<span class="kw">SELECT</span> id, username, role\n<span class="kw">FROM</span> users\n<span class="kw">WHERE</span> username = <span class="str">'${colored}'</span>`;
  document.getElementById('l1rows').innerHTML = '';
}

async function do1() {
  const u = document.getElementById('l1u').value;
  const res = await fetch('/api/l1',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({u})});
  const d = await res.json();
  setSQL(d.sql, u);
  const el = document.getElementById('r1');
  el.style.display = 'block';

  // Update live preview with result table
  let tblHTML = '';
  if (d.ok && d.rows.length) {
    tblHTML = `<table class="sql-result-tbl"><thead><tr>${d.cols.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>`;
    d.rows.forEach(r => { tblHTML += `<tr>${r.map(c=>`<td>${c}</td>`).join('')}</tr>`; });
    tblHTML += '</tbody></table>';
  }
  document.getElementById('l1rows').innerHTML = tblHTML;

  if (d.ok && d.rows.length > 1) {
    el.className = 'lresult ok';
    el.innerHTML = `✅ Baza zwróciła <strong>${d.rows.length} użytkowników</strong> naraz! Udało się!`;
    markSolved(0);
  } else if (d.ok && d.rows.length === 1) {
    el.className = 'lresult ok';
    el.innerHTML = `Zalogowano jako: <strong>${d.rows[0][1]}</strong>. Spróbuj wyciągnąć WSZYSTKICH użytkowników!`;
  } else {
    el.className = 'lresult err';
    el.textContent = '❌ ' + (d.error || 'Nie znaleziono użytkownika.');
  }
}

// ── L2: Numeric UNION ──
const icons = ['🖊️','📓','🎒','🖥️','⌚','📱','🎧','💡'];
async function do2() {
  const id = document.getElementById('l2id').value;
  const res = await fetch('/api/l2',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});
  const d = await res.json();
  setSQL(d.sql, id);
  const err=document.getElementById('e2'), grid=document.getElementById('g2'), lbl=document.getElementById('lbl2');
  if (!d.ok) { err.style.display='block'; err.textContent='⚠️ Błąd SQL: '+d.error; grid.innerHTML=''; return; }
  err.style.display='none';
  if (!d.rows.length) { lbl.textContent='Brak wyników dla tego ID.'; grid.innerHTML=''; return; }
  lbl.textContent = `Wyniki dla ID = ${id}:`;
  grid.innerHTML = d.rows.map((r,i)=>{
    const name = String(r[1]||r[0]||'');
    const price = r[2];
    const isLeak = name.includes('@') || name.includes('H@') || name.includes('!') || (typeof price === 'string' && price.includes('admin'));
    return `<div class="scard ${isLeak?'alert':''}">
      <div class="sico">${icons[i%icons.length]}</div>
      <div class="snm">${name}</div>
      <div class="spr">${price !== null && price !== undefined ? price : '—'}</div>
    </div>`;
  }).join('');
  // Win: haslo admina pojawia sie w wynikach
  const allText = d.rows.flat().join(' ');
  if (allText.includes('H@slo') || allText.includes('admin')) markSolved(1);
}

// ── L3: Admin login ──
async function do3() {
  const u=document.getElementById('l3u').value, p=document.getElementById('l3p').value;
  const res=await fetch('/api/l3',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({u,p})});
  const d=await res.json();
  setSQL(d.sql, u);
  const el=document.getElementById('r3');
  el.style.display='block';
  if (d.ok) {
    el.className='lresult ok';
    el.innerHTML=`✅ Zalogowano jako: <strong>${d.user}</strong> (rola: ${d.role})`;
    markSolved(2);
  } else {
    el.className='lresult err';
    el.textContent='❌ '+d.error;
  }
}

// ── L4: Blog UNION 3 kol ──
async function do4() {
  const q=document.getElementById('l4q').value;
  const res=await fetch('/api/l4',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q})});
  const d=await res.json();
  setSQL(d.sql, q);
  const err=document.getElementById('e4'), arts=document.getElementById('arts'), lbl=document.getElementById('lbl4');
  if (!d.ok) { err.style.display='block'; err.textContent='⚠️ Błąd: '+d.error; arts.innerHTML=''; return; }
  err.style.display='none';
  if (!d.rows.length) { lbl.textContent='Brak artykułów pasujących do zapytania.'; arts.innerHTML=''; return; }
  lbl.textContent=`Znaleziono ${d.rows.length} wynik(ów):`;
  arts.innerHTML=d.rows.map(r=>{
    const title=String(r[1]||''), content=String(r[2]||'');
    const isFlag=title.includes('FLAG')||content.includes('FLAG')||title.includes('Kod');
    return `<div class="article ${isFlag?'flag':''}">
      <div class="atitle">${title}</div>
      <div class="acontent">${content}</div>
      ${isFlag?'<div class="ameta">⚠️ Ten wpis nie powinien tu być!</div>':'<div class="ameta">ID: '+r[0]+'</div>'}
    </div>`;
  }).join('');
  if (d.rows.some(r=>String(r[1]).includes('FLAG')||String(r[2]).includes('FLAG'))) markSolved(3);
}

// ── L5: Kurier UNION 4 kol ──
async function do5() {
  const id=document.getElementById('l5id').value.trim();
  const res=await fetch('/api/l5',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id})});
  const d=await res.json();
  setSQL(d.sql, id);
  const err=document.getElementById('e5'), tr=document.getElementById('tr5');
  if (!d.ok) { err.style.display='block'; err.textContent='⚠️ Błąd: '+d.error; tr.innerHTML=''; return; }
  err.style.display='none';
  if (!d.rows.length) { tr.innerHTML='<div class="trackempty">🔍 Nie znaleziono przesyłki o tym numerze.</div>'; return; }
  const statusIcon = s => s==='W drodze'?'🚚':s==='Dostarczona'?'✅':s==='W sortowni'?'📦':'⚠️';
  tr.innerHTML=d.rows.map(r=>{
    const tid=String(r[0]||''), status=String(r[1]||''), dest=String(r[2]||''), est=String(r[3]||'');
    const isLeak=tid.includes('admin')||status.includes('H@')||dest.includes('admin')||status.includes('user');
    return `<div class="pkgcard ${isLeak?'alert':''}">
      <div class="pkgid">Nr przesyłki: <strong>${tid}</strong></div>
      <div class="pkgstatus">${isLeak?'⚠️':statusIcon(status)} ${status}</div>
      <div class="pkgdet">📍 ${dest}</div>
      <div class="pkgdet" style="margin-top:4px">📅 ${est}</div>
    </div>`;
  }).join('');
  const allText=d.rows.flat().join(' ');
  if (allText.includes('H@slo')||allText.includes('admin')) markSolved(4);
}

// Init
previewSQL();
go(0);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    print("\n" + "="*60)
    print("  🔐  SQL INJECTION QUEST — v3")
    print("="*60)
    print("  ➜  http://localhost:5000")
    print("="*60)
    print()
    print("  5 scenariuszy, 5 różnych technik:")
    print()
    print("  L1 🎓  Tutorial      — ' OR '1'='1  (SQL widoczny na żywo)")
    print("  L2 🛒  Sklep         — numeric UNION SELECT (bez apostrofów!)")
    print("  L3 🔒  Admin panel   — komentarz '--' (tu i tylko tu!)")
    print("  L4 📰  Blog          — UNION SELECT, 3 kolumny")
    print("  L5 📦  Kurier        — UNION SELECT, 4 kolumny (!)")
    print()
    init_db()
    app.run(debug=False, port=5000)