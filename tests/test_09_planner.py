def test_planner_decomposition():
    from agent.planner import Planner
    p = Planner()
    plan = p.create_plan("Build URL shortener")
    assert len(plan["tasks"]) > 0