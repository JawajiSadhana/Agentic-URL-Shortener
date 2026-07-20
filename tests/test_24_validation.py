def test_validation_acceptance():
    from agent.reviewer import Reviewer
    r = Reviewer()
    assert "passed" in r.validate("agent/llm.py")