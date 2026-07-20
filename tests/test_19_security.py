def test_security_scan():
    from agent.llm import llm
    assert llm.scan_secrets("sk-123") == True