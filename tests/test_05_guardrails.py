def test_guardrail_block_path():
    from agent.guardrails import Guardrails
    g = Guardrails()
    res = g.check({"tool": "file_write", "args": {"path": "/etc/passwd"}})
    assert res == False