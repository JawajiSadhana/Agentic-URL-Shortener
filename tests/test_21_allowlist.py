def test_allowlist_paths():
    from agent.guardrails import Guardrails
    g = Guardrails()
    assert "app/" in g.ALLOWLIST