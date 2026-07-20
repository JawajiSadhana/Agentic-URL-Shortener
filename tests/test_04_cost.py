def test_cost_tracking():
    from agent.llm import llm
    llm.call("test prompt", "reasoning")
    assert llm.token_usage["expensive"] > 0