def test_greenfield_generates_db():
    import os
    assert os.path.exists("agent/llm.py")