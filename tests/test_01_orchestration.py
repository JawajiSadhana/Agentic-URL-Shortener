def test_orchestrator_init():
    from agent.orchestrator import Orchestrator
    o = Orchestrator()
    assert o.planner and o.executor
