from agent.traces import log
class Reviewer:
    def validate(self, artifact_path):
        log("reviewer_start", {"path": artifact_path})
        code = open(artifact_path, "r", encoding="utf-8").read()
        checks = {"has_clicks": "clicks INTEGER" in code, "has_response_model": "response_model" in code}
        passed = all(checks.values())
        result = {"passed": passed, "checks": checks}
        log("reviewer_done", result)
        return result