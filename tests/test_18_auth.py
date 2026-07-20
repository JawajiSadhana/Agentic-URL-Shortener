def test_auth_code_generation():
    from agent.llm import llm
    assert "require_auth" in llm.get_auth_code()