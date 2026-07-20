def test_api_endpoints_defined():
    code = open("agent/llm.py").read()
    assert "/shorten" in code and "/analytics" in code