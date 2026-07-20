import sqlite3, secrets, string
from pathlib import Path

DB_PATH = Path("urls.db")

def gen():
    return ''.join(secrets.choice(string.ascii_letters+string.digits) for _ in range(6))

def init_db():
    conn=sqlite3.connect(DB_PATH)
    conn.execute("CREATE TABLE IF NOT EXISTS urls (id INTEGER PRIMARY KEY, original_url TEXT, short_code TEXT UNIQUE, clicks INTEGER DEFAULT 0)")
    conn.commit()
    conn.close()

def create_url(u,c):
    conn=sqlite3.connect(DB_PATH)
    try:
        conn.execute("INSERT INTO urls (original_url, short_code) VALUES (?,?)",(u,c))
        conn.commit()
        return c
    except:
        return None
    finally:
        conn.close()

def get_url(c):
    conn=sqlite3.connect(DB_PATH)
    cur=conn.execute("SELECT original_url FROM urls WHERE short_code=?",(c,))
    r=cur.fetchone()
    if r:
        conn.execute("UPDATE urls SET clicks=clicks+1 WHERE short_code=?",(c,))
        conn.commit()
    conn.close()
    return r[0] if r else None

def get_analytics_by_code(c):
    conn=sqlite3.connect(DB_PATH)
    cur=conn.execute("SELECT short_code, original_url, clicks FROM urls WHERE short_code=?",(c,))
    r=cur.fetchone()
    conn.close()
    return {"code":r[0],"url":r[1],"clicks":r[2]} if r else None