def test_budget_enforcement():
    from agent.llm import llm
    assert llm.BUDGET == 10000