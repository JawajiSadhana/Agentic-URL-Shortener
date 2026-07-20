def test_reviewer_checks():
    from agent.reviewer import Reviewer
    r = Reviewer()
    assert hasattr(r, "validate")