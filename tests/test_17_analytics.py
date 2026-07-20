def test_analytics_function():
    code = open("agent/llm.py").read()
    assert "get_analytics_by_code" in code