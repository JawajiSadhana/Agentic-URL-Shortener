def test_brownfield_auth_task():
    from agent.llm import llm
    res = llm.call("Add JWT auth")
    assert any(t["tool"] == "code_edit" for t in res["tasks"])