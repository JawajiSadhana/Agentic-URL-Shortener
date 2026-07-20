def test_llm_mock_injection():
    from agent.llm import llm
    res = llm.call("Build URL shortener")
    assert "tasks" in res