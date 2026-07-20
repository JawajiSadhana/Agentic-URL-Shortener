from agent.traces import log
import re
class Guardrails:
    RISK_TIERS = {"file_write": "write", "code_edit": "write", "shell": "destructive", "code_search": "read", "test_runner": "read"}
    ALLOWLIST = ["app/", "tests/", "scenarios/"]
    def check(self, task):
        tool = task["tool"]; args = str(task["args"])
        if self.RISK_TIERS.get(tool) == "destructive": log("guardrail_approval", task); return "approval_required"
        if tool in ["file_write", "code_edit"]:
            path = task["args"]["path"]
            if not any(path.startswith(p) for p in self.ALLOWLIST): log("guardrail_blocked", {"reason": "Path not allowed", "path": path}); return False
        if re.search(r'(sk-|api[_-]?key|password)', args, re.I): log("guardrail_blocked", {"reason": "Secret detected"}); return False
        return True