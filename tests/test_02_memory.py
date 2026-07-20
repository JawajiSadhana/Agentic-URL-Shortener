def test_memory_persistence():
    from agent.memory import Memory
    m = Memory()
    m.save_task("t1", None, {"tool": "test"}, {"result": "ok"})
    assert m.get_summary()["tasks_done"] >= 1