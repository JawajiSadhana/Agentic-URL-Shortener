def test_db_has_clicks():
    code = open("agent/llm.py").read()
    assert "clicks INTEGER" in code