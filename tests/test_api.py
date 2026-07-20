import sys, os
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
