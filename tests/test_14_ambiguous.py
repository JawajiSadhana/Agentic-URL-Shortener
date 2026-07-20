def test_ambiguous_detection():
    from agent.planner import Planner
    p = Planner()
    plan = p.create_plan("Add analytics")
    assert plan.get("needs_clarification") == False 
    assert "tasks" in plan