import json
def test_trace_format():
    from agent.traces import log
    log("test_event", {"data": 1})
    with open("logs/ENGINEERING_SUMMARY.jsonl") as f:
        e = json.loads(f.readline())
    assert "id" in e and "parent" in e and "timestamp" in e