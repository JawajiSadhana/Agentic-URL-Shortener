import json
from agent.traces import log

class LLM:
    def __init__(self):
        self.token_usage = {"cheap": 0, "expensive": 0}
        self.BUDGET = 10000

    def count_tokens(self, text: str) -> int:
        return int(len(text.split()) * 1.3)

    def route_model(self, task_tool: str) -> str:
        return "cheap" if task_tool in ["code_search", "shell", "test_runner"] else "expensive"

    def reason(self, prompt):
        steps = []
        if "shortener" in prompt.lower():
            steps.append("Need DB for persistence and redirect")
        if "analytics" in prompt.lower():
            steps.append("Need clicks counter and analytics endpoint")
        if "auth" in prompt.lower():
            steps.append("Need JWT middleware")
        log("llm_reasoning", {"steps": steps})
        return steps

    def call(self, prompt: str, task_tool: str = "reasoning") -> dict:
        self.reason(prompt)
        model_tier = self.route_model(task_tool)
        tokens = self.count_tokens(prompt)
        self.token_usage[model_tier] += tokens
        total = self.token_usage["cheap"] + self.token_usage["expensive"]
        if total > self.BUDGET:
            raise Exception(f"Token budget {self.BUDGET} exceeded")
        log("token_usage", {"tier": model_tier, "tokens": tokens}, cost=tokens)

        if "jwt" in prompt.lower() or "auth" in prompt.lower():
            return {"intent": "add_auth", "tasks": [
                {"tool": "file_write", "args": {"path": "app/auth.py", "content": self.get_auth_code()}},
                {"tool": "code_edit", "args": {"path": "app/main.py", "find": "from app.db import", "replace": "from app.db import\nfrom app.auth import require_auth"}},
                {"tool": "code_edit", "args": {"path": "app/main.py", "find": "def shorten", "replace": "@require_auth\ndef shorten"}},
                {"tool": "test_runner", "args": {}}
            ]}

        risks = ["Scale", "Collision"] if "shortener" in prompt else []
        return {
            "intent": "create_url_shortener" if "shortener" in prompt else "modify",
            "tasks": [
                {"tool": "code_search", "args": {"query": "FastAPI SQLite"}},
                {"tool": "file_write", "args": {"path": "app/db.py", "content": self.get_db_code(), "evidence": ["sqlite docs"]}},
                {"tool": "file_write", "args": {"path": "app/__init__.py", "content": ""}},
                {"tool": "file_write", "args": {"path": "app/main.py", "content": self.get_full_app_code()}},
                {"tool": "file_write", "args": {"path": "tests/test_api.py", "content": self.get_test_code()}},
                {"tool": "test_runner", "args": {}}
            ],
            "risks": risks,
            "mitigations": ["Use Postgres + UUID later"]
        }

    def get_auth_code(self):
        return '''from fastapi import Depends
def require_auth(): return True'''

    def get_db_code(self):
        return '''import sqlite3, secrets, string
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
    return {"code":r[0],"url":r[1],"clicks":r[2]} if r else None'''

    def get_full_app_code(self):
        return '''from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
from pydantic import BaseModel, HttpUrl
from contextlib import asynccontextmanager
from app.db import init_db, create_url, get_url, get_analytics_by_code, gen

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app=FastAPI(lifespan=lifespan)

class URLRequest(BaseModel):
    url: HttpUrl
    custom_alias: str=None

class AnalyticsItem(BaseModel):
    code: str
    url: str
    clicks: int

@app.get("/health")
def health():
    return {"ok":True}

@app.post("/shorten")
def shorten(req: URLRequest):
    code=req.custom_alias or gen()
    if len(code)>10:
        raise HTTPException(400,"Too long")
    if not create_url(str(req.url),code):
        raise HTTPException(409,"Exists")
    return {"short_url":f"/{code}"}

@app.get("/{code}")
def redirect(code: str):
    url=get_url(code)
    if not url:
        raise HTTPException(404)
    return RedirectResponse(url)

@app.get("/analytics/{code}", response_model=AnalyticsItem)
def analytics(code: str):
    d=get_analytics_by_code(code)
    if not d:
        raise HTTPException(404)
    return d'''

    def get_test_code(self):
        return '''import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from fastapi.testclient import TestClient
from app.main import app
c=TestClient(app)

def test_health():
    assert c.get("/health").status_code==200

def test_shorten():
    r = c.post("/shorten", json={"url": "https://google.com"})
    assert r.status_code == 200
    assert "short_url" in r.json()
'''

    def scan_secrets(self, text):
        return "sk-" in text

llm = LLM()