def test_executor_tools():
    from agent.executor import Executor
    e = Executor()
    assert "file_write" in e.tools