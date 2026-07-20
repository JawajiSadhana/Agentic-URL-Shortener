def test_secret_blocking():
    from agent.guardrails import Guardrails
    g = Guardrails()
    res = g.check({"tool": "file_write", "args": {"path": "app/x.py", "content": "api_key=sk-123"}})
    assert res == False