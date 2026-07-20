def test_all_tools_present():
    from agent.executor import Executor
    e = Executor()
    assert set(e.tools.keys()) == {"file_write", "code_edit", "code_search", "shell", "test_runner"}