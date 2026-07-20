def test_retry_cap():
    from agent.orchestrator import Orchestrator
    o = Orchestrator()
    assert o.retry_cap == 2