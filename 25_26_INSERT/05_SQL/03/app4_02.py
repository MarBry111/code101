from flask import Flask, request, jsonify, render_template_string
import sqlite3

app = Flask(__name__)
_db = None

def init_db():
    global _db
    _db = sqlite3.connect("file::memory:?cache=shared", uri=True, check_same_thread=False)
    cur = _db.cursor()
    cur.executescript("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT
        );
        INSERT INTO users VALUES (1,'admin','H@slo_Admina!2024','admin');
        INSERT INTO users VALUES (2,'janek','kotek123','user');
        INSERT INTO users VALUES (3,'ania','piesek456','user');
        INSERT INTO users VALUES (4,'bartek','dragon789','user');
        INSERT INTO users VALUES (5,'bibliotekarka','ksiazka2024','librarian');
        INSERT INTO users VALUES (6,'p.kowalski','matematyka!1','teacher');

        -- 3 kolumny: id, name, price (L2 + L4-sub1)
        CREATE TABLE products (
            id INTEGER PRIMARY KEY, name TEXT, price REAL
        );
        INSERT INTO products VALUES (1,'Dlugopis Parker',29.99);
        INSERT INTO products VALUES (2,'Zeszyt A5',4.50);
        INSERT INTO products VALUES (3,'Plecak Nike',159.00);
        INSERT INTO products VALUES (4,'Kalkulator Casio',49.00);
        INSERT INTO products VALUES (5,'[TAJNY] Voucher VIP',999.00);

        -- 3 kolumny: id, title, content (L4-sub0, sub2)
        CREATE TABLE articles (
            id INTEGER PRIMARY KEY, title TEXT, content TEXT, author TEXT
        );
        INSERT INTO articles VALUES (1,'Jak sie uczyc SQL','SQL to jezyk baz danych uzywany wszedzie.','J. Kowalski');
        INSERT INTO articles VALUES (2,'Python dla poczatkujacych','Python jest prosty i potezny.','A. Nowak');
        INSERT INTO articles VALUES (3,'Cyberbezpieczenstwo','Chronmy swoje dane w sieci!','T. Wisniewski');

        -- 3 kolumny jak articles: id, code, description  (cel dla L4)
        CREATE TABLE secret_codes (
            id INTEGER PRIMARY KEY, code TEXT, description TEXT
        );
        INSERT INTO secret_codes VALUES (1,'FLAG{UNION_M4ST3R}','Kod mistrza UNION');
        INSERT INTO secret_codes VALUES (2,'FLAG{SQL_H4CK3R}','Kod hakera SQL');

        -- 4 kolumny: tracking_id, status, destination, estimated (L5-sub0)
        CREATE TABLE packages (
            id INTEGER PRIMARY KEY,
            tracking_id TEXT, status TEXT, destination TEXT, estimated TEXT
        );
        INSERT INTO packages VALUES (1,'PKG-001','W drodze','Warszawa ul. Kwiatowa 5','2024-12-20');
        INSERT INTO packages VALUES (2,'PKG-002','Dostarczona','Krakow ul. Dluga 12','2024-12-18');
        INSERT INTO packages VALUES (3,'PKG-003','W sortowni','Gdansk ul. Morska 3','2024-12-21');

        -- 4 kolumny: order_ref, item, status, date (L5-sub1)
        CREATE TABLE orders (
            id INTEGER PRIMARY KEY,
            order_ref TEXT, item TEXT, status TEXT, date TEXT
        );
        INSERT INTO orders VALUES (1,'ZAM-001','Laptop Dell XPS','W realizacji','2024-12-15');
        INSERT INTO orders VALUES (2,'ZAM-002','Mysz Logitech','Wysłano','2024-12-14');
        INSERT INTO orders VALUES (3,'ZAM-003','Monitor 27"','Oczekuje','2024-12-16');

        -- 4 kolumny: emp_id, name, dept, position (L5-sub2)
        CREATE TABLE employees (
            id INTEGER PRIMARY KEY,
            emp_id TEXT, name TEXT, dept TEXT, position TEXT
        );
        INSERT INTO employees VALUES (1,'EMP-001','Jan Kowalski','IT','Programista');
        INSERT INTO employees VALUES (2,'EMP-002','Anna Nowak','HR','Rekruter');
        INSERT INTO employees VALUES (3,'EMP-003','Piotr Wisniewski','Finance','Ksiegowy');
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

# ══ L1: OR injection (SQL visible, tutorial) ══════════════════
# sub 0: szkolny portal – pobierz WSZYSTKICH userow
# sub 1: forum       – zaloguj TYLKO jako admin  (OR username='admin'--)
# sub 2: strefa VIP  – omiń filtr AND role='user' (admin nie pasuje, trzeba OR)
@app.route("/api/l1", methods=["POST"])
def l1():
    d = request.get_json()
    u, sub = d.get("u",""), d.get("sub",0)
    if sub == 2:
        sql = f"SELECT id, username, role FROM users WHERE username = '{u}' AND role = 'user'"
    else:
        sql = f"SELECT id, username, role FROM users WHERE username = '{u}'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql, "rows": [], "cols": []})
    return jsonify({"ok": True, "sql": sql, "rows": r["rows"], "cols": r["cols"]})

# ══ L2: Numeric injection (brak apostrofow) ════════════════════
# sub 0: katalog – pokaż WSZYSTKIE produkty (1 OR 1=1)
# sub 1: profil  – UNION wyciągnij hasło admina z users
# sub 2: oceny   – UNION wyciągnij secret_codes
@app.route("/api/l2", methods=["POST"])
def l2():
    d = request.get_json()
    pid, sub = d.get("id","1"), d.get("sub",0)
    sql = f"SELECT id, name, price FROM products WHERE id != 5 AND id = {pid} "
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql, "rows": [], "cols": []})
    return jsonify({"ok": True, "sql": sql, "rows": r["rows"], "cols": r["cols"]})

# ══ L3: Komentarz -- (pomiń hasło) ════════════════════════════
# sub 0: CMS firmowy   – admin'--
# sub 1: Biblioteka    – bibliotekarka'--
# sub 2: Dziennik el.  – p.kowalski'--
@app.route("/api/l3", methods=["POST"])
def l3():
    d = request.get_json()
    u, p = d.get("u",""), d.get("p","")
    sql = f"SELECT id, username, role FROM users WHERE username = '{u}' AND password = '{p}'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql})
    if r["rows"]:
        row = r["rows"][0]
        return jsonify({"ok": True, "user": row[1], "role": row[2], "sql": sql})
    return jsonify({"ok": False, "error": "Nieprawidłowy login lub hasło.", "sql": sql})

# ══ L4: UNION SELECT 3 kolumny ════════════════════════════════
# sub 0: blog       – SELECT id,title,content FROM articles → UNION secret_codes
# sub 1: sklep      – SELECT id,name,price FROM products   → UNION users (id,username,password)
# sub 2: FAQ/forum  – SELECT id,title,content FROM articles (LIKE content) → UNION packages (tracking_id,status,destination)
@app.route("/api/l4", methods=["POST"])
def l4():
    d = request.get_json()
    q, sub = d.get("q",""), d.get("sub",0)
    if sub == 1:
        sql = f"SELECT id, name, price FROM products WHERE name LIKE '%{q}%'"
    elif sub == 2:
        sql = f"SELECT id, title, content FROM articles WHERE content LIKE '%{q}%'"
    else:
        sql = f"SELECT id, title, content FROM articles WHERE title LIKE '%{q}%'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql, "rows": [], "cols": []})
    return jsonify({"ok": True, "sql": sql, "rows": r["rows"], "cols": r["cols"]})

# ══ L5: UNION SELECT 4 kolumny ════════════════════════════════
# sub 0: kurier    – SELECT tracking_id,status,destination,estimated FROM packages → UNION users (username,password,role,id)
# sub 1: zamówienia– SELECT order_ref,item,status,date FROM orders              → UNION secret_codes + NULL (id,code,description,NULL)
# sub 2: HR portal – SELECT emp_id,name,dept,position FROM employees             → UNION articles (id,title,content,author)
@app.route("/api/l5", methods=["POST"])
def l5():
    d = request.get_json()
    tid, sub = d.get("id",""), d.get("sub",0)
    if sub == 1:
        sql = f"SELECT order_ref, item, status, date FROM orders WHERE order_ref = '{tid}'"
    elif sub == 2:
        sql = f"SELECT emp_id, name, dept, position FROM employees WHERE emp_id = '{tid}'"
    else:
        sql = f"SELECT tracking_id, status, destination, estimated FROM packages WHERE tracking_id = '{tid}'"
    r = run_sql(sql)
    if not r["ok"]:
        return jsonify({"ok": False, "error": r["error"], "sql": sql, "rows": [], "cols": []})
    return jsonify({"ok": True, "sql": sql, "rows": r["rows"], "cols": r["cols"]})

# ══════════════════════════════════════════════════════════════
HTML = r"""
<!DOCTYPE html>
<html lang="pl">
<head>
<meta charset="UTF-8">
<title>SQL Injection Quest</title>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{font-family:'Inter',sans-serif;background:#0d1117;color:#e2e8f0;height:100vh;display:flex;flex-direction:column;overflow:hidden}

/* TOPBAR */
.tb{background:#161b22;border-bottom:1px solid #21262d;padding:0 16px;height:48px;display:flex;align-items:center;gap:10px;flex-shrink:0}
.tb-title{font-family:'JetBrains Mono',monospace;font-size:.75rem;color:#58a6ff;letter-spacing:1px;white-space:nowrap}
.tabs{display:flex;gap:3px;margin-left:auto}
.tab{background:none;border:1px solid #30363d;border-radius:6px;color:#8b949e;padding:3px 11px;font-size:.74rem;font-family:'Inter',sans-serif;cursor:pointer;transition:all .15s;white-space:nowrap}
.tab:hover{border-color:#58a6ff;color:#cdd9e5}
.tab.active{background:#1f3558;border-color:#388bfd;color:#e2e8f0}
.tab.done{border-color:#238636;color:#3fb950}
.tab.done.active{background:#0d2b1f;border-color:#3fb950}
.score{font-family:'JetBrains Mono',monospace;font-size:.74rem;color:#d29922;background:rgba(210,153,34,.1);border:1px solid rgba(210,153,34,.3);border-radius:20px;padding:3px 11px;margin-left:8px;white-space:nowrap}

/* WORKSPACE */
.ws{flex:1;display:grid;grid-template-columns:1fr 370px;overflow:hidden}

/* APP WINDOW */
.aw{display:flex;flex-direction:column;overflow:hidden;border-right:1px solid #21262d}
.chrome{background:#1c2128;border-bottom:1px solid #21262d;padding:7px 12px;display:flex;align-items:center;gap:9px;flex-shrink:0}
.dots{display:flex;gap:5px}
.dots span{width:10px;height:10px;border-radius:50%}
.dr{background:#ff5f56}.dy{background:#ffbd2e}.dg{background:#27c93f}
.urlbar{flex:1;background:#0d1117;border:1px solid #30363d;border-radius:5px;padding:4px 11px;font-family:'JetBrains Mono',monospace;font-size:.7rem;color:#8b949e;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}
.frame{flex:1;overflow-y:auto}
.pg{display:none;min-height:100%}
.pg.active{display:block}

/* ── Shared form styles (light bg apps) ── */
/* All text on white/light backgrounds MUST be explicitly dark */
.light-input{
  width:100%;border:1.5px solid #d1d5db;border-radius:7px;padding:9px 12px;
  font-size:.88rem;font-family:'Inter',sans-serif;outline:none;
  color:#111827 !important;background:#fff;transition:border-color .2s
}
.light-input:focus{border-color:var(--accent,#6366f1)}
.light-label{display:block;font-size:.78rem;font-weight:600;color:#374151 !important;margin-bottom:5px}
.lbtn{width:100%;border:none;border-radius:8px;padding:10px;font-size:.88rem;font-weight:700;cursor:pointer;font-family:'Inter',sans-serif;color:#fff;transition:opacity .2s;margin-top:6px}
.lbtn:hover{opacity:.88}
.fg{margin-bottom:14px}
.msg{margin-top:12px;border-radius:7px;padding:9px 12px;font-size:.83rem;display:none}
.msg.err{background:#fef2f2;color:#b91c1c !important;border:1px solid #fca5a5}
.msg.ok{background:#f0fdf4;color:#15803d !important;border:1px solid #86efac}

/* ─── L1: Tutorial ─── */
.tut-bg{min-height:100%;display:flex;flex-direction:column;align-items:center;padding:24px 20px;gap:16px;background:#f0f2f5}
.tut-card{background:#fff;border-radius:12px;box-shadow:0 2px 16px rgba(0,0,0,.1);width:100%;max-width:440px;overflow:hidden}
.tut-card-hdr{padding:18px 22px}
.tut-card-hdr h2{color:#fff !important;font-size:1.05rem;font-weight:700}
.tut-card-hdr p{color:rgba(255,255,255,.75) !important;font-size:.78rem;margin-top:3px}
.tut-card-body{padding:18px 22px}
/* SQL Preview */
.sqlprev-card{background:#fff;border-radius:12px;box-shadow:0 2px 16px rgba(0,0,0,.1);width:100%;max-width:440px;overflow:hidden}
.sqlprev-hdr{background:#1e1e2e;padding:9px 14px;display:flex;align-items:center;gap:8px;font-family:'JetBrains Mono',monospace;font-size:.68rem;color:#6272a4}
.sqlprev-hdr .badge{background:#50fa7b;color:#1e1e2e;border-radius:4px;padding:1px 7px;font-size:.62rem;font-weight:700}
.sqlprev-body{background:#282a36;padding:12px 14px;font-family:'JetBrains Mono',monospace;font-size:.76rem;line-height:1.9;word-break:break-all;min-height:60px}
.kw{color:#ff79c6}.str{color:#f1fa8c}.inj{color:#ff5555;font-weight:700;text-decoration:underline dotted}
/* Result table in tutorial - dark bg, light text */
.rtbl{width:100%;border-collapse:collapse;font-family:'JetBrains Mono',monospace;font-size:.74rem;margin-top:0}
.rtbl th{background:#44475a;color:#f8f8f2 !important;padding:6px 10px;text-align:left;font-weight:600}
.rtbl td{padding:6px 10px;border-bottom:1px solid #383a4a;color:#f8f8f2 !important;background:#282a36}
.rtbl tr:last-child td{border-bottom:none}

/* ─── L2: E-sklep ─── */
.shop{background:#f3f4f6;min-height:100%}
.shopnav{background:#fff;border-bottom:1px solid #e5e7eb;padding:0 18px;height:50px;display:flex;align-items:center;gap:12px;position:sticky;top:0;z-index:5}
.shopbrand{font-weight:900;font-size:1rem;color:#7c3aed}
.shopbrand span{color:#f59e0b}
.idform{margin-left:auto;display:flex;align-items:center;gap:7px}
.idform label{font-size:.78rem;color:#6b7280 !important;font-weight:500}
.idform input{border:1.5px solid #d1d5db;border-radius:6px;padding:5px 9px;font-size:.83rem;font-family:'JetBrains Mono',monospace;width:90px;outline:none;color:#111827 !important;background:#fff}
.idform input:focus{border-color:#7c3aed}
.idform button{background:#7c3aed;color:#fff;border:none;border-radius:6px;padding:5px 13px;font-size:.82rem;font-weight:600;cursor:pointer}
.shopbody{padding:18px}
.pgrid{display:grid;grid-template-columns:repeat(auto-fill,minmax(145px,1fr));gap:11px;margin-top:11px}
.pcard{background:#fff;border-radius:10px;padding:14px 12px;border:1px solid #e5e7eb;text-align:center}
.pcard.alert{border-color:#ef4444;background:#fef2f2}
.pcard .pico{font-size:1.6rem;margin-bottom:7px}
.pcard .pnm{font-size:.79rem;font-weight:600;color:#111827 !important;margin-bottom:4px}
.pcard .ppr{font-size:.9rem;font-weight:700;color:#7c3aed !important}
.pcard.alert .pnm{color:#991b1b !important}
.pcard.alert .ppr{color:#991b1b !important}
.sherr{background:#fef2f2;color:#b91c1c !important;border:1px solid #fca5a5;border-radius:7px;padding:8px 12px;font-size:.8rem;margin-bottom:10px;display:none}
.shoplbl{font-size:.82rem;color:#6b7280 !important;margin-top:4px}

/* ─── L3: Admin/Login variant ─── */
.loginbg{min-height:100%;display:flex;align-items:center;justify-content:center;padding:40px 20px}
.logincard{border-radius:14px;padding:34px 38px;width:350px}
.logincard .logo{text-align:center;margin-bottom:22px}
.logincard .logo .ico{font-size:2rem}
.logincard .logo h2{font-size:1.05rem;font-weight:700;margin-top:7px}
.logincard .logo p{font-size:.76rem;margin-top:3px}

/* Dark login (admin, CMS) */
.logincard.dark{background:#1e2235;border:1px solid #2d3555;box-shadow:0 20px 50px rgba(0,0,0,.5)}
.logincard.dark .logo h2{color:#e2e8f0 !important}
.logincard.dark .logo p{color:#64748b !important}
.logincard.dark .light-label{color:#94a3b8 !important}
.logincard.dark .light-input{background:#0f172a !important;border-color:#2d3555 !important;color:#e2e8f0 !important}
.logincard.dark .light-input:focus{border-color:#6366f1 !important}
.logincard.dark .msg.err{background:#2d1515;color:#f87171 !important;border-color:#7f1d1d}
.logincard.dark .msg.ok{background:#0d2b1a;color:#4ade80 !important;border-color:#14532d}
.admin-warn{background:#291a04;border:1px solid #78350f;border-radius:7px;padding:9px 12px;font-size:.74rem;color:#fbbf24 !important;margin-bottom:16px}

/* Light login (library, teacher) */
.logincard.light{background:#fff;border:1px solid #e5e7eb;box-shadow:0 4px 24px rgba(0,0,0,.08)}
.logincard.light .logo h2{color:#111827 !important}
.logincard.light .logo p{color:#6b7280 !important}
.logincard.light .msg.err{background:#fef2f2;color:#b91c1c !important;border-color:#fca5a5}
.logincard.light .msg.ok{background:#f0fdf4;color:#15803d !important;border-color:#86efac}

/* ─── L4: Blog / Shop / FAQ ─── */
.blog{background:#f9fafb;min-height:100%}
.blognav{background:#fff;border-bottom:1px solid #e5e7eb;padding:0 18px;height:50px;display:flex;align-items:center;gap:12px;position:sticky;top:0;z-index:5}
.blognav .brand{font-weight:800;font-size:.95rem}
.bsearchw{display:flex;gap:6px;margin-left:auto}
.bsearchw input{border:1.5px solid #d1d5db;border-radius:7px;padding:6px 11px;font-size:.82rem;font-family:'Inter',sans-serif;width:170px;outline:none;color:#111827 !important;background:#fff}
.bsearchw input:focus{border-color:#111}
.bsearchw button{background:#111;color:#fff;border:none;border-radius:7px;padding:6px 13px;font-size:.8rem;font-weight:600;cursor:pointer}
.blogbody{padding:18px 22px}
.bloglbl{font-size:.82rem;color:#6b7280 !important;margin-bottom:12px}
.acard{background:#fff;border-radius:10px;border:1px solid #e5e7eb;padding:14px 16px;margin-bottom:10px}
.acard.flag{border-color:#f59e0b;background:#fffbeb}
.acard .atitle{font-size:.92rem;font-weight:700;color:#111827 !important;margin-bottom:4px}
.acard .acontent{font-size:.81rem;color:#4b5563 !important;line-height:1.6}
.acard .ameta{font-size:.7rem;color:#9ca3af !important;margin-top:7px}
.acard.flag .atitle{color:#92400e !important}
.acard.flag .acontent{color:#78350f !important}
.blogerr{background:#fef2f2;color:#b91c1c !important;border:1px solid #fca5a5;border-radius:7px;padding:8px 12px;font-size:.8rem;margin-bottom:11px;display:none}

/* ─── L5: Kurier / Zamówienia / HR ─── */
.tracker{background:#eef2f7;min-height:100%}
.trackernav{padding:0 18px;height:50px;display:flex;align-items:center;gap:10px}
.trackernav .brand{font-weight:800;font-size:.95rem;color:#fff;letter-spacing:.5px}
.trackform{max-width:480px;margin:24px auto 0;background:#fff;border-radius:12px;padding:22px 26px;box-shadow:0 4px 18px rgba(0,0,0,.08)}
.trackform h3{font-size:.95rem;font-weight:700;color:#111827 !important;margin-bottom:5px}
.trackform p{font-size:.79rem;color:#6b7280 !important;margin-bottom:14px}
.trackrow{display:flex;gap:7px}
.trackinput{flex:1;border:2px solid #d1d5db;border-radius:8px;padding:9px 13px;font-size:.88rem;font-family:'JetBrains Mono',monospace;outline:none;color:#111827 !important;background:#fff;letter-spacing:.5px;text-transform:uppercase}
.trackinput:focus{border-color:var(--tnav-color,#1a56db)}
.trackbtn{background:var(--tnav-color,#1a56db);color:#fff;border:none;border-radius:8px;padding:9px 18px;font-size:.85rem;font-weight:700;cursor:pointer;font-family:'Inter',sans-serif}
.trackerr{background:#fef2f2;color:#b91c1c !important;border:1px solid #fca5a5;border-radius:7px;padding:9px 12px;font-size:.8rem;margin-top:13px;display:none}
.tresult{margin-top:18px}
.tcard{background:#f8fafc;border-radius:9px;border:1px solid #e2e8f0;padding:14px;margin-bottom:9px}
.tcard.alert{border-color:#ef4444;background:#fef2f2}
.tcard .tid{font-family:'JetBrains Mono',monospace;font-size:.77rem;color:#64748b !important;margin-bottom:5px}
.tcard .tstatus{font-size:.9rem;font-weight:700;color:#111827 !important;margin-bottom:3px}
.tcard .tdet{font-size:.78rem;color:#4b5563 !important;margin-top:3px}
.tcard.alert .tstatus{color:#991b1b !important}
.tcard.alert .tdet{color:#991b1b !important}
.tempty{text-align:center;padding:28px;font-size:.83rem;color:#9ca3af !important}

/* RIGHT PANEL */
.panel{display:flex;flex-direction:column;overflow:hidden;background:#161b22}
.phdr{padding:10px 15px;border-bottom:1px solid #21262d;font-size:.68rem;font-family:'JetBrains Mono',monospace;color:#8b949e;text-transform:uppercase;letter-spacing:1px;flex-shrink:0}
.pbody{flex:1;overflow-y:auto;padding:13px;display:flex;flex-direction:column;gap:10px}
.pc{background:#1c2128;border:1px solid #21262d;border-radius:9px;overflow:hidden}
.pch{padding:8px 12px;font-size:.67rem;font-family:'JetBrains Mono',monospace;color:#8b949e;border-bottom:1px solid #21262d;text-transform:uppercase;letter-spacing:1px}
.pcb{padding:10px 12px;font-size:.8rem;line-height:1.75;color:#8b949e}
.pcb code{font-family:'JetBrains Mono',monospace;background:#0d1117;color:#79c0ff;padding:1px 5px;border-radius:4px;font-size:.73rem}
.pcb strong{color:#cdd9e5}
/* Task list */
.tasklist{list-style:none;display:flex;flex-direction:column;gap:5px;padding:10px 12px}
.titem{display:flex;align-items:center;gap:8px;padding:7px 10px;border-radius:7px;cursor:pointer;transition:all .15s;border:1px solid transparent}
.titem:hover{background:rgba(255,255,255,.04);border-color:#30363d}
.titem.active{background:#1f3558;border-color:#388bfd}
.titem.tdone{border-color:#238636}
.titem .tnum{font-family:'JetBrains Mono',monospace;font-size:.68rem;color:#484f58;width:16px;flex-shrink:0}
.titem.active .tnum{color:#58a6ff}
.titem .tlabel{font-size:.79rem;color:#8b949e;flex:1;line-height:1.4}
.titem.active .tlabel{color:#e2e8f0}
.titem.tdone .tlabel{color:#3fb950}
.titem .tcheck{font-size:.85rem;color:#3fb950;opacity:0;width:14px}
.titem.tdone .tcheck{opacity:1}
/* Tech badge */
.tbadge{display:inline-block;background:rgba(56,139,253,.12);border:1px solid rgba(56,139,253,.3);color:#79c0ff;border-radius:5px;padding:2px 8px;font-size:.69rem;font-family:'JetBrains Mono',monospace;margin-bottom:8px}
.locked{text-align:center;padding:22px 12px}
.locked .lico{font-size:1.6rem;margin-bottom:7px}
.locked p{font-size:.79rem;line-height:1.6;color:#484f58}
.suc{background:rgba(63,185,80,.07);border:1px solid rgba(63,185,80,.25);border-radius:9px;padding:12px;text-align:center;display:none}
.suc.show{display:block}
.suc h4{color:#3fb950;font-size:.86rem;margin-bottom:4px}
.suc p{font-size:.77rem;color:#8b949e;line-height:1.5}

/* SQL LOG */
.sqllog{border-top:1px solid #21262d;padding:9px 13px;font-family:'JetBrains Mono',monospace;font-size:.67rem;flex-shrink:0;min-height:50px;max-height:88px;overflow-y:auto;background:#0d1117}
.sqllog .lbl{color:#484f58;margin-bottom:3px}
.sqltxt{color:#6e7681;word-break:break-all;line-height:1.65}
.sqltxt .inj{color:#f85149;font-weight:700}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-thumb{background:#21262d;border-radius:4px}
</style>
</head>
<body>

<div class="tb">
  <div class="tb-title">🔐 SQL INJECTION QUEST</div>
  <div class="tabs">
    <button class="tab active" onclick="gotoLv(0)" id="tab0">🎓 Tutorial</button>
    <button class="tab" onclick="gotoLv(1)" id="tab1">🛒 Sklep</button>
    <button class="tab" onclick="gotoLv(2)" id="tab2">🔒 Logowanie</button>
    <button class="tab" onclick="gotoLv(3)" id="tab3">📰 Wyszukiwarka</button>
    <button class="tab" onclick="gotoLv(4)" id="tab4">📦 Systemy</button>
  </div>
  <div class="score" id="score">⭐ 0 / 15</div>
</div>

<div class="ws">
<!-- ══════════ LEFT ══════════ -->
<div class="aw">
  <div class="chrome">
    <div class="dots"><span class="dr"></span><span class="dy"></span><span class="dg"></span></div>
    <div class="urlbar" id="urlbar">http://szkolnyportal.pl/login</div>
  </div>
  <div class="frame">

    <!-- ══ L1: Tutorial (3 sub) ══ -->
    <div class="pg active" id="pg0">
      <div class="tut-bg">
        <div class="tut-card">
          <div class="tut-card-hdr" id="l1hdr" style="background:#4f46e5">
            <h2 id="l1title">🏫 Szkolny Portal</h2>
            <p id="l1sub">Wpisz swoją nazwę użytkownika</p>
          </div>
          <div class="tut-card-body">
            <div class="fg">
              <label class="light-label" id="l1lbl">Nazwa użytkownika</label>
              <input class="light-input" id="l1u" type="text" placeholder="np. janek"
                     oninput="previewL1()" onkeydown="if(event.key==='Enter')doL1()" style="--accent:#4f46e5">
            </div>
            <button class="lbtn" id="l1btn" style="background:#4f46e5" onclick="doL1()">Wejdź →</button>
            <div class="msg" id="l1msg"></div>
          </div>
        </div>
        <div class="sqlprev-card">
          <div class="sqlprev-hdr"><span class="badge">DEBUG</span>Zapytanie SQL budowane na żywo:</div>
          <div class="sqlprev-body" id="l1prev"></div>
          <div style="background:#282a36;padding:0 14px 12px" id="l1tbl"></div>
        </div>
      </div>
    </div>

    <!-- ══ L2: Sklep (3 sub, same UI) ══ -->
    <div class="pg" id="pg1">
      <div class="shop">
        <div class="shopnav">
          <div class="shopbrand" id="l2brand">Sklep<span>MAX</span></div>
          <div class="idform">
            <label id="l2lbl">ID produktu:</label>
            <input id="l2id" type="text" value="1" onkeydown="if(event.key==='Enter')doL2()">
            <button onclick="doL2()">Pokaż</button>
          </div>
        </div>
        <div class="shopbody">
          <div class="sherr" id="l2err"></div>
          <div class="shoplbl" id="l2info">Wpisz ID produktu w pasku</div>
          <div class="pgrid" id="l2grid"></div>
        </div>
      </div>
    </div>

    <!-- ══ L3: Login wariant (3 sub, zmienia sie wyglad) ══ -->
    <div class="pg" id="pg2">
      <div class="loginbg" id="l3bg">
        <div class="logincard dark" id="l3card">
          <div class="logo">
            <div class="ico" id="l3ico">🏛️</div>
            <h2 id="l3title">Panel CMS</h2>
            <p id="l3subtitle">Dostęp tylko dla uprawnionych</p>
          </div>
          <div class="admin-warn" id="l3warn">⚠️ Nieautoryzowany dostęp jest zabroniony</div>
          <div class="fg">
            <label class="light-label" id="l3lbl1">Login</label>
            <input class="light-input" id="l3u" type="text" placeholder="login..." onkeydown="if(event.key==='Enter')doL3()">
          </div>
          <div class="fg">
            <label class="light-label">Hasło</label>
            <input class="light-input" id="l3p" type="password" placeholder="••••••••" onkeydown="if(event.key==='Enter')doL3()">
          </div>
          <button class="lbtn" id="l3btn" onclick="doL3()">Zaloguj →</button>
          <div class="msg" id="l3msg"></div>
        </div>
      </div>
    </div>

    <!-- ══ L4: Wyszukiwarka (3 sub, 2 UI-warianty) ══ -->
    <div class="pg" id="pg3">
      <!-- sub 0 i 2: blog/FAQ -->
      <div id="l4blog" class="blog">
        <div class="blognav">
          <div class="brand" id="l4brand" style="color:#111">TechPortal<span style="color:#ef4444">.</span>pl</div>
          <div style="font-size:.78rem;color:#6b7280;display:flex;gap:12px;margin-left:14px">
            <span id="l4nav1">Aktualności</span><span id="l4nav2">Tutoriale</span><span id="l4nav3">Forum</span>
          </div>
          <div class="bsearchw">
            <input id="l4q" type="text" placeholder="Szukaj..." onkeydown="if(event.key==='Enter')doL4()">
            <button onclick="doL4()">Szukaj</button>
          </div>
        </div>
        <div class="blogbody">
          <div class="blogerr" id="l4err"></div>
          <div class="bloglbl" id="l4lbl">Wpisz frazę do wyszukania</div>
          <div id="l4arts"></div>
        </div>
      </div>
      <!-- sub 1: sklep search -->
      <div id="l4shop" class="shop" style="display:none">
        <div class="shopnav">
          <div class="shopbrand">Sklep<span>ABC</span></div>
          <div style="margin-left:auto;display:flex;gap:7px">
            <input class="light-input" style="width:170px;padding:6px 10px" id="l4sq" type="text"
                   placeholder="Szukaj produktu..." onkeydown="if(event.key==='Enter')doL4()">
            <button class="idform" onclick="doL4()" style="background:#7c3aed;color:#fff;border:none;border-radius:6px;padding:5px 13px;font-size:.82rem;font-weight:600;cursor:pointer">Szukaj</button>
          </div>
        </div>
        <div class="shopbody">
          <div class="sherr" id="l4serr"></div>
          <div class="shoplbl" id="l4slbl">Wpisz nazwę produktu</div>
          <div class="pgrid" id="l4sgrid"></div>
        </div>
      </div>
    </div>

    <!-- ══ L5: Systemy (3 sub, 3 UI-warianty) ══ -->
    <div class="pg" id="pg4">
      <!-- sub 0: kurier -->
      <div id="l5courier" class="tracker" style="--tnav-color:#1a56db">
        <div class="trackernav" style="background:#1a56db"><div class="brand">SWIFT<span style="opacity:.6">EX</span></div><div style="margin-left:auto;font-size:.73rem;color:rgba(255,255,255,.6)">Śledzenie przesyłek</div></div>
        <div style="padding:18px">
          <div class="trackform">
            <h3>Śledź przesyłkę</h3>
            <p>Podaj numer nadania z listu przewozowego</p>
            <div class="trackrow">
              <input class="trackinput" id="l5id0" type="text" placeholder="PKG-001" onkeydown="if(event.key==='Enter')doL5()">
              <button class="trackbtn" onclick="doL5()">Sprawdź</button>
            </div>
            <div style="font-size:.7rem;color:#9ca3af;margin-top:6px">Przykłady: PKG-001, PKG-002, PKG-003</div>
            <div class="trackerr" id="l5e0"></div>
            <div class="tresult" id="l5r0"></div>
          </div>
        </div>
      </div>
      <!-- sub 1: zamówienia -->
      <div id="l5orders" class="tracker" style="display:none;--tnav-color:#059669">
        <div class="trackernav" style="background:#059669"><div class="brand">ORDER<span style="opacity:.6">TRACK</span></div><div style="margin-left:auto;font-size:.73rem;color:rgba(255,255,255,.6)">Status zamówień</div></div>
        <div style="padding:18px">
          <div class="trackform">
            <h3>Sprawdź zamówienie</h3>
            <p>Wpisz numer zamówienia z potwierdzenia</p>
            <div class="trackrow">
              <input class="trackinput" id="l5id1" type="text" placeholder="ZAM-001" onkeydown="if(event.key==='Enter')doL5()">
              <button class="trackbtn" style="background:#059669" onclick="doL5()">Sprawdź</button>
            </div>
            <div style="font-size:.7rem;color:#9ca3af;margin-top:6px">Przykłady: ZAM-001, ZAM-002, ZAM-003</div>
            <div class="trackerr" id="l5e1"></div>
            <div class="tresult" id="l5r1"></div>
          </div>
        </div>
      </div>
      <!-- sub 2: HR portal -->
      <div id="l5hr" class="tracker" style="display:none;--tnav-color:#9333ea">
        <div class="trackernav" style="background:#9333ea"><div class="brand">HR<span style="opacity:.6">PORTAL</span></div><div style="margin-left:auto;font-size:.73rem;color:rgba(255,255,255,.6)">Dane pracowników</div></div>
        <div style="padding:18px">
          <div class="trackform">
            <h3>Znajdź pracownika</h3>
            <p>Wpisz numer ID pracownika z karty</p>
            <div class="trackrow">
              <input class="trackinput" id="l5id2" type="text" placeholder="EMP-001" onkeydown="if(event.key==='Enter')doL5()">
              <button class="trackbtn" style="background:#9333ea" onclick="doL5()">Znajdź</button>
            </div>
            <div style="font-size:.7rem;color:#9ca3af;margin-top:6px">Przykłady: EMP-001, EMP-002, EMP-003</div>
            <div class="trackerr" id="l5e2"></div>
            <div class="tresult" id="l5r2"></div>
          </div>
        </div>
      </div>
    </div>

  </div><!-- /frame -->
</div><!-- /aw -->

<!-- ══════════ RIGHT PANEL ══════════ -->
<div class="panel">
  <div class="phdr">📋 zadania i opis</div>
  <div class="pbody" id="pb"></div>
  <div class="sqllog">
    <div class="lbl">// ostatnie zapytanie SQL:</div>
    <div class="sqltxt" id="sqlog">— brak —</div>
  </div>
</div>
</div><!-- /ws -->

<script>
// ═══════════════════════════════════════════════
// DANE POZIOMÓW I ZADAŃ
// ═══════════════════════════════════════════════
const LEVELS = [
  // L1 — OR injection (SQL visible)
  {
    title: "🎓 Tutorial — OR injection",
    badge: "' OR '1'='1  /  ' OR username='admin'--",
    showHint: true,
    hint: `Apostrof <code>'</code> <strong>wyrywa się</strong> ze stringa SQL i zamyka go. Potem możesz dołożyć własny warunek.<br><br>
<code>OR '1'='1</code> → warunek zawsze prawdziwy (wszyscy userzy)<br>
<code>OR username='admin'--</code> → tylko admin, komentarz ucina resztę`,
    tasks: [
      {
        title: "Pokaż WSZYSTKICH użytkowników",
        url: "http://szkolnyportal.pl/login",
        desc: `Normalny formularz logowania szkołnego portalu.<br><br>
SQL wygląda tak: <code>WHERE username = '{twój input}'</code><br><br>
Użyj OR żeby baza zwróciła <strong>wszystkich</strong> użytkowników naraz zamiast jednego.`,
        win: d => d.rows.length > 1
      },
      {
        title: "Zaloguj TYLKO jako admin",
        url: "http://forum.szkolne.pl/login",
        desc: `Tym razem cel jest precyzyjny: chcesz wejść <strong>dokładnie</strong> jako admin, nie zwracać wszystkich.<br><br>
Spróbuj: czy możesz napisać OR który wyciągnie tylko użytkownika o konkretnej nazwie?<br><br>
Musisz zakończyć zapytanie komentarzem!`,
        win: d => d.rows.length > 0 && d.rows.some(r => r[2] === 'admin')
      },
      {
        title: "Omiń filtr 'tylko zwykli userzy'",
        url: "http://strefaVIP.pl/dostep",
        desc: `Ten formularz ma dodatkowy warunek — pokazuje tylko użytkowników z <code>role='user'</code>.<br><br>
SQL: <code>WHERE username='{input}' AND role='user'</code><br><br>
Admin ma role='admin' — normalnie nie pojawi się. Jak go wyciągnąć mimo tego filtra?`,
        win: d => d.rows.some(r => r[2] === 'admin')
      }
    ]
  },
  // L2 — Numeric injection
  {
    title: "🛒 Sklep — Numeric injection",
    badge: "1 OR 1=1  /  0 UNION SELECT ...",
    showHint: false,
    hint: null,
    tasks: [
      {
        title: "Odkryj ukryty produkt (#5)",
        url: "http://sklepmax.pl/produkt?id=1",
        desc: `Sklep wyświetla produkty po numerze ID. Wpisz 1, 2, 3, 4 — zobaczysz normalne produkty.<br><br>
SQL: <code>WHERE id = {twój input}</code><br><br>
Brak apostrofów! Liczba wchodzi bezpośrednio do SQL.<br>
W sklepie jest 5. produkt ukryty — spraw żeby się pojawił.`,
        win: d => d.rows.length > 4
      },
      {
        title: "Wyciągnij hasło admina (UNION)",
        url: "http://sklepmax.pl/produkt?id=1",
        desc: `Tym razem skorzystaj z UNION SELECT żeby zamiast produktów zobaczyć dane z tabeli <code>users</code>.<br><br>
Tabela users ma kolumny: <code>id, username, password</code><br>
SELECT produktów ma 3 kolumny: <code>id, name, price</code><br><br>
Podpowiedź: zacznij od <code>0</code> żeby produkty się nie mieszały.`,
        win: d => d.rows.some(r => String(r[1]).includes('admin') || String(r[2]).includes('H@slo'))
      },
      {
        title: "Wyciągnij tajne kody (UNION)",
        url: "http://sklepmax.pl/produkt?id=1",
        desc: `Teraz cel to tabela <code>secret_codes</code> z kolumnami <code>id, code, description</code>.<br><br>
Ta sama technika co poprzednio — UNION SELECT z numerycznym ID — ale inny cel.<br><br>
Szukaj: kody zawierają tekst <code>FLAG{...}</code>`,
        win: d => d.rows.some(r => String(r[1]).includes('FLAG') || String(r[2]).includes('FLAG'))
      }
    ]
  },
  // L3 — Comment --
  {
    title: "🔒 Logowanie — Komentarz --",
    badge: "admin'--  /  bibliotekarka'--",
    showHint: false,
    hint: null,
    tasks: [
      {
        title: "Panel CMS — zaloguj jako admin",
        url: "http://cms.firmaxyz.pl/admin",
        desc: `Firmowy panel CMS sprawdza login i hasło:<br>
<code>WHERE username='{u}' AND password='{p}'</code><br><br>
Znasz login: <code>admin</code>. Hasło nieznane.<br>
SQL ma specjalny znak komentarza — wszystko po nim jest ignorowane. Znajdź go!`,
        win: d => d.ok && d.role === 'admin'
      },
      {
        title: "Biblioteka — wejdź jako bibliotekarka",
        url: "http://biblioteka-szkolna.pl/panel",
        desc: `Szkolna biblioteka — ten sam mechanizm co CMS, ale inny użytkownik.<br><br>
Login bibliotekarki: <code>bibliotekarka</code><br>
Hasło? Nieznane. Użyj tej samej techniki co poprzednio.<br><br>
Uwaga: tym razem powinno zalogować jako <strong>librarian</strong>, nie admin.`,
        win: d => d.ok && d.role === 'librarian'
      },
      {
        title: "Dziennik szkolny — wejdź jako nauczyciel",
        url: "http://dziennik.szkola.pl/login",
        desc: `Elektroniczny dziennik szkolny — kolejny system z tym samym błędem.<br><br>
Login nauczyciela: <code>p.kowalski</code><br>
Haselko? Nieznane — ale już wiesz co zrobić. 😏<br><br>
Udaj się do systemu jako teacher.`,
        win: d => d.ok && d.role === 'teacher'
      }
    ]
  },
  // L4 — UNION 3 cols
  {
    title: "📰 Wyszukiwarka — UNION 3 kolumny",
    badge: "' UNION SELECT a,b,c FROM tabela--",
    showHint: false,
    hint: null,
    tasks: [
      {
        title: "Blog: wyciągnij tajne kody FLAG",
        url: "http://techportal.pl/search",
        desc: `Wyszukiwarka bloga: <code>SELECT id, title, content FROM articles WHERE title LIKE '%{q}%'</code><br><br>
W bazie jest tabela <code>secret_codes</code> z kolumnami <code>id, code, description</code>.<br><br>
Użyj UNION SELECT żeby kody FLAG pojawiły się jako "artykuły".<br>
Pamiętaj: UNION wymaga tej samej liczby kolumn → tutaj <strong>3</strong>.`,
        win: d => d.rows.some(r => String(r[1]).includes('FLAG') || String(r[2]).includes('FLAG'))
      },
      {
        title: "Sklep: wyciągnij hasła użytkowników",
        url: "http://sklepabc.pl/szukaj",
        desc: `Wyszukiwarka sklepu: <code>SELECT id, name, price FROM products WHERE name LIKE '%{q}%'</code><br><br>
Tym razem cel: tabela <code>users</code> z kolumnami <code>id, username, password</code>.<br><br>
Pasują te same 3 kolumny → klasyczny UNION SELECT.<br>
Wykradnij hasła użytkowników przez wyszukiwarkę sklepu!`,
        win: d => d.rows.some(r => String(r[2]).includes('H@slo') || String(r[2]).includes('kotek') || String(r[2]).includes('piesek'))
      },
      {
        title: "FAQ: wyciągnij dane przesyłek",
        url: "http://techportal.pl/faq",
        desc: `FAQ portalu: <code>SELECT id, title, content FROM articles WHERE content LIKE '%{q}%'</code><br><br>
Tym razem szukaj w <strong>treści</strong> (content), nie tytule — ta sama tabela, inna kolumna w WHERE.<br><br>
Cel: tabela <code>packages</code> — ale ma 5 kolumn. Musisz wybrać tylko 3:<br>
<code>tracking_id, status, destination</code>`,
        win: d => d.rows.some(r => String(r[1]).startsWith('PKG') || String(r[2]).includes('W drodze') || String(r[2]).includes('Dostarczona'))
      }
    ]
  },
  // L5 — UNION 4 cols
  {
    title: "📦 Systemy — UNION 4 kolumny",
    badge: "' UNION SELECT a,b,c,d FROM tabela--",
    showHint: false,
    hint: null,
    tasks: [
      {
        title: "Kurier: wykradnij dane użytkowników",
        url: "http://swiftex.pl/tracking",
        desc: `System śledzenia: <code>SELECT tracking_id, status, destination, estimated FROM packages WHERE tracking_id = '{id}'</code><br><br>
<strong>4 kolumny!</strong> To trudniejsze — UNION musi też mieć 4.<br><br>
Cel: tabela <code>users</code> — wybierz 4 odpowiadające kolumny.<br>
Wpisz najpierw <code>PKG-001</code> żeby zobaczyć normalny wynik.`,
        win: d => d.rows.some(r => String(r[0]).includes('admin') || String(r[1]).includes('H@slo'))
      },
      {
        title: "Zamówienia: wyciągnij kody + NULL",
        url: "http://ordertrack.pl/status",
        desc: `System zamówień: <code>SELECT order_ref, item, status, date FROM orders WHERE order_ref = '{id}'</code><br><br>
Cel: tabela <code>secret_codes</code> — ale ma tylko 3 kolumny!<br>
Jak dopasować do 4? Musisz dołożyć <strong>czwartą kolumnę ręcznie</strong> — wpisz <code>NULL</code> lub dowolny tekst jako czwartą.<br><br>
Przykład: <code>UNION SELECT id, code, description, NULL FROM secret_codes--</code>`,
        win: d => d.rows.some(r => String(r[0]).includes('FLAG') || String(r[1]).includes('FLAG'))
      },
      {
        title: "HR Portal: wyciągnij artykuły jako 'pracownicy'",
        url: "http://hrportal.firma.pl/employee",
        desc: `HR Portal: <code>SELECT emp_id, name, dept, position FROM employees WHERE emp_id = '{id}'</code><br><br>
Cel: tabela <code>articles</code> z kolumnami <code>id, title, content, author</code> — dokładnie 4 kolumny!<br><br>
Wpisz najpierw <code>EMP-001</code> żeby zobaczyć normalny wynik.<br>
Teraz spraw żeby artykuły z bloga pojawiły się w HR Portalu jako "pracownicy".`,
        win: d => d.rows.some(r => String(r[1]).includes('SQL') || String(r[1]).includes('Python') || String(r[2]).includes('jezyk'))
      }
    ]
  }
];

// ═══════════════════════════════════════════════
// STATE
// ═══════════════════════════════════════════════
let curLv = 0, curSub = 0;
const solved = new Set(); // "lv-sub" strings

function solvedKey(lv, sub) { return `${lv}-${sub}`; }
function isSolved(lv, sub) { return solved.has(solvedKey(lv, sub)); }

function markSolved(lv, sub) {
  const k = solvedKey(lv, sub);
  if (solved.has(k)) return;
  solved.add(k);
  document.getElementById('score').textContent = `⭐ ${solved.size} / 15`;
  const tabs = ['tab0','tab1','tab2','tab3','tab4'];
  const lvSolved = [0,1,2,3,4].filter(s => isSolved(lv,s));
  if (lvSolved.length === 3) document.getElementById(tabs[lv]).classList.add('done');
  renderPanel();
  const sc = document.getElementById(`sc${lv}`);
  if (sc) sc.classList.add('show');
}

// ═══════════════════════════════════════════════
// NAVIGATION
// ═══════════════════════════════════════════════
function gotoLv(lv) {
  curLv = lv; curSub = 0;
  document.querySelectorAll('.pg').forEach((p,i) => p.classList.toggle('active', i===lv));
  document.querySelectorAll('.tab').forEach((t,i) => t.classList.toggle('active', i===lv));
  applySubContext();
  renderPanel();
}

function gotoSub(sub) {
  curSub = sub;
  applySubContext();
  renderPanel();
}

// ═══════════════════════════════════════════════
// APPLY SUB-TASK CONTEXT TO THE APP UI
// ═══════════════════════════════════════════════
const L1_CTX = [
  { color:'#4f46e5', title:'🏫 Szkolny Portal', sub:'Wpisz swoją nazwę użytkownika', lbl:'Nazwa użytkownika' },
  { color:'#0ea5e9', title:'💬 Forum szkolne', sub:'Zaloguj się do forum', lbl:'Nick użytkownika' },
  { color:'#ea580c', title:'🔥 Strefa Premium', sub:'Dostęp tylko dla wybranych', lbl:'Twój login' }
];
const L3_CTX = [
  { type:'dark', bg:'linear-gradient(135deg,#0f172a,#1e1b4b)', ico:'🏛️', title:'Panel CMS Firmowy', sub:'Dostęp tylko dla administratorów', warn:true, lbl:'Login administratora' },
  { type:'light', bg:'linear-gradient(135deg,#ecfdf5,#d1fae5)', ico:'📚', title:'Biblioteka Szkolna', sub:'Panel bibliotekarza', warn:false, lbl:'Login bibliotekarza' },
  { type:'light', bg:'linear-gradient(135deg,#fff7ed,#ffedd5)', ico:'📖', title:'Dziennik Elektroniczny', sub:'Panel nauczyciela', warn:false, lbl:'Login nauczyciela' }
];
const L4_CTX = [
  { mode:'blog', brand:'TechPortal<span style="color:#ef4444">.</span>pl', n1:'Aktualności', n2:'Tutoriale', n3:'Forum', ph:'Szukaj artykułu...', col:'#111' },
  { mode:'shop' },
  { mode:'blog', brand:'FAQ<span style="color:#3b82f6">Portal</span>.pl', n1:'Pomoc', n2:'FAQ', n3:'Kontakt', ph:'Szukaj w FAQ...', col:'#1d4ed8' }
];
const L5_CTX = ['courier','orders','hr'];

function applySubContext() {
  const task = LEVELS[curLv].tasks[curSub];
  document.getElementById('urlbar').textContent = task.url;

  if (curLv === 0) {
    const ctx = L1_CTX[curSub];
    document.getElementById('l1hdr').style.background = ctx.color;
    document.getElementById('l1title').textContent = ctx.title;
    document.getElementById('l1sub').textContent = ctx.sub;
    document.getElementById('l1lbl').textContent = ctx.lbl;
    document.getElementById('l1btn').style.background = ctx.color;
    document.getElementById('l1u').value = '';
    document.getElementById('l1msg').style.display = 'none';
    previewL1();
  }
  if (curLv === 1) {
    const labels = ['ID produktu:','ID produktu:','ID produktu:'];
    document.getElementById('l2lbl').textContent = labels[curSub];
    document.getElementById('l2id').value = '1';
    document.getElementById('l2err').style.display='none';
    document.getElementById('l2grid').innerHTML='';
    document.getElementById('l2info').textContent='Wpisz ID w pasku powyżej';
  }
  if (curLv === 2) {
    const ctx = L3_CTX[curSub];
    const card = document.getElementById('l3card');
    card.className = `logincard ${ctx.type}`;
    document.getElementById('l3bg').style.background = ctx.bg;
    document.getElementById('l3ico').textContent = ctx.ico;
    document.getElementById('l3title').textContent = ctx.title;
    document.getElementById('l3subtitle').textContent = ctx.sub;
    document.getElementById('l3warn').style.display = ctx.warn ? 'block':'none';
    document.getElementById('l3lbl1').textContent = ctx.lbl;
    document.getElementById('l3u').value=''; document.getElementById('l3p').value='';
    document.getElementById('l3msg').style.display='none';
    const colors=['#6366f1','#10b981','#f97316'];
    document.getElementById('l3btn').style.background = colors[curSub];
  }
  if (curLv === 3) {
    const ctx = L4_CTX[curSub];
    const blogDiv = document.getElementById('l4blog');
    const shopDiv = document.getElementById('l4shop');
    if (ctx.mode === 'shop') {
      blogDiv.style.display='none'; shopDiv.style.display='block';
      document.getElementById('l4sq').value='';
      document.getElementById('l4serr').style.display='none';
      document.getElementById('l4sgrid').innerHTML='';
      document.getElementById('l4slbl').textContent='Wpisz nazwę produktu';
    } else {
      blogDiv.style.display='block'; shopDiv.style.display='none';
      document.getElementById('l4brand').innerHTML = ctx.brand;
      document.getElementById('l4brand').style.color = ctx.col;
      document.getElementById('l4nav1').textContent=ctx.n1;
      document.getElementById('l4nav2').textContent=ctx.n2;
      document.getElementById('l4nav3').textContent=ctx.n3;
      document.getElementById('l4q').placeholder=ctx.ph;
      document.getElementById('l4q').value='';
      document.getElementById('l4err').style.display='none';
      document.getElementById('l4arts').innerHTML='';
      document.getElementById('l4lbl').textContent='Wpisz frazę do wyszukania';
    }
  }
  if (curLv === 4) {
    ['l5courier','l5orders','l5hr'].forEach((id,i) => {
      document.getElementById(id).style.display = i===curSub?'block':'none';
    });
    [`l5r0`,`l5r1`,`l5r2`].forEach(id => { const e=document.getElementById(id); if(e) e.innerHTML=''; });
    [`l5e0`,`l5e1`,`l5e2`].forEach(id => { const e=document.getElementById(id); if(e) e.style.display='none'; });
  }
}

// ═══════════════════════════════════════════════
// PANEL RENDER
// ═══════════════════════════════════════════════
function renderPanel() {
  const lv = LEVELS[curLv];
  const taskListHTML = lv.tasks.map((t,i) => `
    <li class="titem ${i===curSub?'active':''} ${isSolved(curLv,i)?'tdone':''}" onclick="gotoSub(${i})">
      <span class="tnum">${i+1}.</span>
      <span class="tlabel">${t.title}</span>
      <span class="tcheck">✓</span>
    </li>`).join('');

  const task = lv.tasks[curSub];
  let html = `
    <div class="pc">
      <div class="pch">🗂️ zadania — ${lv.title}</div>
      <ul class="tasklist">${taskListHTML}</ul>
    </div>
    <div class="pc">
      <div class="pch">🎯 aktywne zadanie</div>
      <div class="pcb">${task.desc}</div>
    </div>
    <div class="pc">
      <div class="pch">🔧 technika</div>
      <div class="pcb">
        <div class="tbadge">${lv.badge}</div>
        ${lv.showHint && lv.hint
          ? `<br>${lv.hint}`
          : `<div class="locked"><div class="lico">🔐</div><p>Odkryj samodzielnie!<br>Wskazówka ukryta.</p></div>`}
      </div>
    </div>
    <div class="suc ${isSolved(curLv,curSub)?'show':''}" id="sc${curLv}">
      <h4>✅ Zadanie ${curSub+1} zaliczone!</h4>
      <p>Świetna robota! Przejdź do kolejnego zadania →</p>
    </div>`;
  document.getElementById('pb').innerHTML = html;
}

// ═══════════════════════════════════════════════
// SQL LOG
// ═══════════════════════════════════════════════
function setSQL(sql, inj) {
  const el = document.getElementById('sqlog');
  const e = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  if (inj && sql.includes(inj)) {
    el.innerHTML = e(sql).replace(e(inj), `<span class="inj">${e(inj)}</span>`);
  } else { el.textContent = sql; }
}

// ═══════════════════════════════════════════════
// L1 — Live SQL preview
// ═══════════════════════════════════════════════
function previewL1() {
  const u = document.getElementById('l1u').value;
  const e = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
  const eu = e(u)
    .replace(/&#x27;|'/g, m => `<span class="inj">'</span>`)
    .replace(/--/g, `<span class="inj">--</span>`)
    .replace(/\bOR\b/gi, m => `<span style="color:#ffb86c">${m}</span>`)
    .replace(/\bUNION\b/gi, m => `<span style="color:#ffb86c">${m}</span>`)
    .replace(/\bSELECT\b/gi, m => `<span class="kw">${m}</span>`);
  const suffix = curSub === 2 ? ` <span class="kw">AND</span> role = <span class="str">'user'</span>` : '';
  document.getElementById('l1prev').innerHTML =
    `<span class="kw">SELECT</span> id, username, role\n<span class="kw">FROM</span> users\n<span class="kw">WHERE</span> username = <span class="str">'${eu}'</span>${suffix}`;
  document.getElementById('l1tbl').innerHTML = '';
}

async function doL1() {
  const u = document.getElementById('l1u').value;
  const r = await fetch('/api/l1',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({u,sub:curSub})});
  const d = await r.json();
  setSQL(d.sql, u);
  const msg = document.getElementById('l1msg');
  msg.style.display='block';
  // Result table in dark preview
  let tbl = '';
  if (d.ok && d.rows.length) {
    tbl = `<table class="rtbl"><thead><tr>${d.cols.map(c=>`<th>${c}</th>`).join('')}</tr></thead><tbody>`;
    d.rows.forEach(row => { tbl += `<tr>${row.map(c=>`<td>${c}</td>`).join('')}</tr>`; });
    tbl += '</tbody></table>';
    document.getElementById('l1tbl').innerHTML = tbl;
    msg.className='msg ok'; msg.innerHTML=`✅ Baza zwróciła <strong>${d.rows.length}</strong> wiersz(y)`;
  } else if (!d.ok) {
    document.getElementById('l1tbl').innerHTML='';
    msg.className='msg err'; msg.textContent='❌ Błąd SQL: '+d.error;
  } else {
    document.getElementById('l1tbl').innerHTML='';
    msg.className='msg err'; msg.textContent='❌ Brak wyników';
  }
  if (d.ok && LEVELS[0].tasks[curSub].win(d)) markSolved(0, curSub);
}

// ═══════════════════════════════════════════════
// L2 — Numeric injection
// ═══════════════════════════════════════════════
const pIco = ['🖊️','📓','🎒','🖥️','🏆','💼','📚','🖌️','⌚','💡'];
async function doL2() {
  const id = document.getElementById('l2id').value;
  const r = await fetch('/api/l2',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,sub:curSub})});
  const d = await r.json();
  setSQL(d.sql, id);
  const err=document.getElementById('l2err'),grid=document.getElementById('l2grid'),lbl=document.getElementById('l2info');
  if (!d.ok){ err.style.display='block'; err.textContent='⚠️ Błąd SQL: '+d.error; grid.innerHTML=''; return; }
  err.style.display='none';
  if (!d.rows.length){ lbl.textContent='Brak wyników dla tego ID.'; grid.innerHTML=''; return; }
  lbl.textContent=`Wyniki dla ID = ${id} (${d.rows.length} rekord/y):`;
  grid.innerHTML=d.rows.map((row,i)=>{
    const nm=String(row[1]??''), pr=row[2];
    const isAlert=nm.includes('H@slo')||nm.includes('FLAG')||nm.includes('admin')||nm.includes('kotek')|| nm.includes('dragon')||(typeof pr==='string'&&pr.length>10);
    return `<div class="pcard ${isAlert?'alert':''}">
      <div class="pico">${pIco[i%pIco.length]}</div>
      <div class="pnm">${nm}</div>
      <div class="ppr">${pr!==null&&pr!==undefined?pr:'-'}</div>
    </div>`;
  }).join('');
  if (LEVELS[1].tasks[curSub].win(d)) markSolved(1, curSub);
}

// ═══════════════════════════════════════════════
// L3 — Comment --
// ═══════════════════════════════════════════════
async function doL3() {
  const u=document.getElementById('l3u').value, p=document.getElementById('l3p').value;
  const r=await fetch('/api/l3',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({u,p,sub:curSub})});
  const d=await r.json();
  setSQL(d.sql, u);
  const msg=document.getElementById('l3msg'); msg.style.display='block';
  if (d.ok){ msg.className='msg ok'; msg.innerHTML=`✅ Zalogowano jako: <strong>${d.user}</strong> (rola: ${d.role})`; }
  else { msg.className='msg err'; msg.textContent='❌ '+d.error; }
  if (LEVELS[2].tasks[curSub].win(d)) markSolved(2, curSub);
}

// ═══════════════════════════════════════════════
// L4 — UNION 3 cols
// ═══════════════════════════════════════════════
async function doL4() {
  const q = curSub===1
    ? document.getElementById('l4sq').value
    : document.getElementById('l4q').value;
  const r=await fetch('/api/l4',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({q,sub:curSub})});
  const d=await r.json();
  setSQL(d.sql, q);

  if (curSub===1) {
    // shop UI
    const err=document.getElementById('l4serr'),grid=document.getElementById('l4sgrid'),lbl=document.getElementById('l4slbl');
    if (!d.ok){ err.style.display='block'; err.textContent='⚠️ Błąd: '+d.error; grid.innerHTML=''; return; }
    err.style.display='none';
    if (!d.rows.length){ lbl.textContent='Brak wyników.'; grid.innerHTML=''; return; }
    lbl.textContent=`Znaleziono ${d.rows.length} wynik(ów):`;
    grid.innerHTML=d.rows.map((row,i)=>{
      const nm=String(row[1]??''), pr=row[2];
      const isAlert=nm.includes('H@slo')||nm.includes('kotek')||nm.includes('dragon')||nm.includes('admin');
      return `<div class="pcard ${isAlert?'alert':''}">
        <div class="pico">${pIco[i%pIco.length]}</div>
        <div class="pnm">${nm}</div>
        <div class="ppr">${pr!==null&&pr!==undefined?pr:'-'}</div>
      </div>`;
    }).join('');
  } else {
    // blog/FAQ UI
    const err=document.getElementById('l4err'),arts=document.getElementById('l4arts'),lbl=document.getElementById('l4lbl');
    if (!d.ok){ err.style.display='block'; err.textContent='⚠️ Błąd: '+d.error; arts.innerHTML=''; return; }
    err.style.display='none';
    if (!d.rows.length){ lbl.textContent='Brak wyników.'; arts.innerHTML=''; return; }
    lbl.textContent=`Znaleziono ${d.rows.length} wynik(ów):`;
    arts.innerHTML=d.rows.map(row=>{
      const title=String(row[1]??''), content=String(row[2]??'');
      const isFlag=title.includes('FLAG')||content.includes('FLAG')||title.includes('Kod');
      const isPkg=title.startsWith('PKG')||content.includes('W drodze')||content.includes('Dostarczona');
      const special=isFlag||isPkg;
      return `<div class="acard ${special?'flag':''}">
        <div class="atitle">${title}</div>
        <div class="acontent">${content}</div>
        <div class="ameta">${special?'⚠️ Ten wpis nie powinien tu być!':'ID: '+row[0]}</div>
      </div>`;
    }).join('');
  }
  if (LEVELS[3].tasks[curSub].win(d)) markSolved(3, curSub);
}

// ═══════════════════════════════════════════════
// L5 — UNION 4 cols
// ═══════════════════════════════════════════════
async function doL5() {
  const inputs=['l5id0','l5id1','l5id2'];
  const id=document.getElementById(inputs[curSub]).value;
  const r=await fetch('/api/l5',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({id,sub:curSub})});
  const d=await r.json();
  setSQL(d.sql, id);
  const errEl=document.getElementById(`l5e${curSub}`), resEl=document.getElementById(`l5r${curSub}`);
  if (!d.ok){ errEl.style.display='block'; errEl.textContent='⚠️ Błąd SQL: '+d.error; resEl.innerHTML=''; return; }
  errEl.style.display='none';
  if (!d.rows.length){ resEl.innerHTML='<div class="tempty">🔍 Brak wyników dla tego ID.</div>'; return; }
  const sico=['🚚','✅','📦','🏭','⚠️'];
  resEl.innerHTML=d.rows.map((row,i)=>{
    const c0=String(row[0]??''),c1=String(row[1]??''),c2=String(row[2]??''),c3=String(row[3]??'');
    const isAlert=c0.includes('admin')||c1.includes('H@slo')||c0.includes('FLAG')||c1.includes('FLAG')||c1.includes('SQL')||c1.includes('Python')||c1.includes('Cyber');
    return `<div class="tcard ${isAlert?'alert':''}">
      <div class="tid">${sico[i%sico.length]} ${c0}</div>
      <div class="tstatus">${c1}</div>
      <div class="tdet">📍 ${c2}</div>
      <div class="tdet">📋 ${c3}</div>
    </div>`;
  }).join('');
  if (LEVELS[4].tasks[curSub].win(d)) markSolved(4, curSub);
}

// ═══════════════════════════════════════════════
// INIT
// ═══════════════════════════════════════════════
previewL1();
gotoLv(0);
</script>
</body>
</html>
"""

if __name__ == "__main__":
    print("\n" + "="*62)
    print("  🔐  SQL INJECTION QUEST — v3 (15 zadań)")
    print("="*62)
    print("  ➜  http://localhost:5001")
    print("="*62)
    print()
    print("  L1 🎓 Tutorial (OR)     3 różne scenariusze, SQL widoczny")
    print("  L2 🛒 Sklep (Numeric)   3 cele: ukryty prod / hasło / kody")
    print("  L3 🔒 Login (--)        3 systemy: CMS / Biblioteka / Dziennik")
    print("  L4 📰 Wyszukiwarka(3k)  3 tabele: kody / hasła / paczki")
    print("  L5 📦 Systemy (4k)      3 syst.: Kurier / Zamówienia / HR")
    print()
    init_db()
    app.run(debug=False, port=5001)