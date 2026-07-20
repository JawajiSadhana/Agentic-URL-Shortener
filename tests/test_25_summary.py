def test_engineering_summary_created():
    import os, json
    if os.path.exists("ENGINEERING_SUMMARY.json"):
        with open("ENGINEERING_SUMMARY.json") as f:
            s = json.load(f)
        assert "plan" in s